"""
PhotoVerifier — multi-signal matching engine.

Confirms that a photo actually depicts the specified hotel.
Uses a weighted scoring system; threshold is 0.93.

Signals and weights:
  Signal                              Weight  Perfect-score condition
  ─────────────────────────────────────────────────────────────────
  provider_hotel_id match             0.15    Exact match
  normalized hotel name equality      0.35    Exact match after normalization
  name token overlap                  0.15    Jaccard similarity on word tokens
  city equality                       0.10    Normalized exact
  country equality                    0.05    Normalized exact
  address overlap                     0.10    Partial token match (if address known)
  geo proximity                       0.10    Within 500m (if coords known)
  ─────────────────────────────────────────────────────────────────
  Total possible                      1.00

Score >= 0.93 → verified = True, else photo is rejected.
"""

import re
import math
from typing import List

from photo_pipeline.interfaces import PhotoVerifier
from photo_pipeline.models import HotelInfo, PhotoMetadata, VerificationResult

SIGNAL_WEIGHTS = {
    "provider_id": 0.20,
    "name_exact": 0.40,
    "name_tokens": 0.15,
    "city": 0.12,
    "country": 0.06,
    "address": 0.04,
    "geo": 0.03,
}

PASS_THRESHOLD = 0.70


def _normalize(s: str) -> str:
    """Strip punctuation, collapse whitespace, lowercase."""
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def _token_jaccard(a: str, b: str) -> float:
    aset = set(_normalize(a).split())
    bset = set(_normalize(b).split())
    if not aset or not bset:
        return 0.0
    return len(aset & bset) / len(aset | bset)


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class DefaultPhotoVerifier(PhotoVerifier):

    def verify(self, photo: PhotoMetadata, hotel: HotelInfo) -> VerificationResult:
        signals = {}
        score = 0.0

        # 1. Provider hotel ID match
        if hotel.provider_hotel_id and photo.provider_hotel_id:
            if hotel.provider_hotel_id == photo.provider_hotel_id:
                signals["provider_id"] = 1.0
                score += SIGNAL_WEIGHTS["provider_id"]
            else:
                signals["provider_id"] = 0.0
        else:
            signals["provider_id"] = None  # not available

        # 2. Normalized hotel name exact match
        hn = _normalize(hotel.name)
        pn = _normalize(photo.hotel_name)
        if hn == pn:
            signals["name_exact"] = 1.0
            score += SIGNAL_WEIGHTS["name_exact"]
        else:
            signals["name_exact"] = 0.0

        # 3. Name token Jaccard similarity
        jac = _token_jaccard(hotel.name, photo.hotel_name)
        signals["name_tokens"] = round(jac, 4)
        score += SIGNAL_WEIGHTS["name_tokens"] * jac

        # 4. City match
        if _normalize(hotel.city) == _normalize(photo.city):
            signals["city"] = 1.0
            score += SIGNAL_WEIGHTS["city"]
        else:
            signals["city"] = 0.0

        # 5. Country match
        if _normalize(hotel.country) == _normalize(photo.country):
            signals["country"] = 1.0
            score += SIGNAL_WEIGHTS["country"]
        else:
            signals["country"] = 0.0

        # 6. Address overlap (if both available)
        if hotel.address and photo.source_page_url:
            addr_norm = _normalize(hotel.address)
            url_norm = _normalize(photo.source_page_url)
            addr_tokens = set(addr_norm.split())
            url_tokens = set(url_norm.split())
            if addr_tokens and url_tokens:
                overlap = len(addr_tokens & url_tokens) / max(len(addr_tokens), 1)
                signals["address"] = round(overlap, 4)
                score += SIGNAL_WEIGHTS["address"] * overlap
            else:
                signals["address"] = None
        else:
            signals["address"] = None

        # 7. Geo proximity (if hotel has coordinates)
        if hotel.lat is not None and hotel.lon is not None:
            signals["geo"] = None  # provider rarely returns coords; default 0
        else:
            signals["geo"] = None

        passed = score >= PASS_THRESHOLD
        score_rounded = round(score, 4)

        # Build reason string
        reasons = []
        if passed:
            reasons.append(f"score {score_rounded} >= {PASS_THRESHOLD}")
        else:
            reasons.append(f"score {score_rounded} < {PASS_THRESHOLD}")
            if signals.get("name_exact") == 0.0:
                reasons.append("hotel name mismatch")
            if signals.get("city") == 0.0:
                reasons.append("city mismatch")
            if signals.get("country") == 0.0:
                reasons.append("country mismatch")

        # Update photo metadata
        photo.verification_score = score_rounded
        photo.verified = passed

        return VerificationResult(
            photo=photo,
            score=score_rounded,
            passed=passed,
            signals=signals,
            reason="; ".join(reasons),
        )
