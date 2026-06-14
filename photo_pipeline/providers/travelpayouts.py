"""
Travelpayouts / Hotellook provider.
Uses the Hotellook static API to look up hotels by location,
then fetches photos via the Hotellook image CDN.

Requires TRAVELPAYOUTS_API_TOKEN in .env.
"""

import os
from typing import List, Optional
from urllib.parse import quote

from photo_pipeline.providers.base import BaseProvider
from photo_pipeline.interfaces import PhotoProvider
from photo_pipeline.models import HotelInfo, PhotoMetadata


class TravelpayoutsProvider(BaseProvider, PhotoProvider):

    provider_name = "travelpayouts"

    def __init__(self):
        self.api_token = os.getenv("TRAVELPAYOUTS_API_TOKEN", "")
        self.marker = os.getenv("TRAVELPAYOUTS_MARKER", "736226")

    def search(self, hotel: HotelInfo) -> List[PhotoMetadata]:
        if not self.api_token:
            return []

        # 1. Search for hotel in Travelpayouts database
        hotel_id = self._resolve_hotel_id(hotel)
        if not hotel_id:
            return []

        # 2. Fetch photos using Hotellook CDN
        return self._fetch_photos(hotel_id, hotel)

    def _resolve_hotel_id(self, hotel: HotelInfo) -> Optional[str]:
        # Try exact lookup via static API
        query = quote(f"{hotel.name} {hotel.city}")
        url = (
            f"https://api.travelpayouts.com/v1/hotel/static/hotels.json"
            f"?token={self.api_token}&query={query}&limit=5"
        )
        data = self._fetch_json(url)
        if not data:
            return None

        hotels_list = data if isinstance(data, list) else data.get("hotels", data.get("data", []))
        if not hotels_list:
            return None

        # Best match: compare normalized name
        best = None
        best_score = 0.0
        nl = hotel.normalized_name()

        for h in hotels_list:
            if not isinstance(h, dict):
                continue
            hn = (h.get("name") or h.get("hotelName") or "").lower().strip()
            score = self._name_similarity(nl, hn)
            # bonus for city match
            hc = (h.get("city") or h.get("location", {})
                  .get("city", "")).lower().strip()
            if hc and hotel.normalized_city() in hc:
                score += 0.1
            if score > best_score:
                best_score = score
                best = h

        if best and best_score >= 0.5:
            return str(best.get("id") or best.get("hotelId") or "")

        return None

    def _name_similarity(self, a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        if a == b:
            return 1.0
        a_parts = set(a.split())
        b_parts = set(b.split())
        if not a_parts or not b_parts:
            return 0.0
        intersection = a_parts & b_parts
        return len(intersection) / max(len(a_parts), len(b_parts))

    def _fetch_photos(self, hotel_id: str, hotel: HotelInfo) -> List[PhotoMetadata]:
        photos = []
        cdn = "https://photo.hotellook.com/image/v2"
        for idx in range(1, 6):
            url = f"{cdn}/{hotel_id}/{idx}.jpg"
            photos.append(PhotoMetadata(
                image_url=url,
                hotel_name=hotel.name,
                city=hotel.city,
                country=hotel.country,
                provider=self.provider_name,
                provider_hotel_id=hotel_id,
                source_page_url=f"https://search.hotellook.com/hotels?id={hotel_id}",
                attribution="Hotellook / Travelpayouts",
                verification_score=0.0,
                verified=False,
                alt_text=f"{hotel.name} — photo {idx}",
                caption=f"{hotel.name}",
            ))
        return photos
