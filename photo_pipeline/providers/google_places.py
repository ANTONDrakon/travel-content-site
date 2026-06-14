"""
Google Places Photos provider.

Uses Places API (Text Search + Place Details) to find a place by name/address/coordinates,
then fetches photos via the Places Photos endpoint.

Requires GOOGLE_API_KEY in .env.
Serves as a fallback — all results are marked unverified until checked by PhotoVerifier.
"""

import os
from typing import List, Optional
from urllib.parse import quote

from photo_pipeline.providers.base import BaseProvider
from photo_pipeline.interfaces import PhotoProvider
from photo_pipeline.models import HotelInfo, PhotoMetadata


class GooglePlacesProvider(BaseProvider, PhotoProvider):

    provider_name = "google_places"

    BASE = "https://maps.googleapis.com/maps/api/place"

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY", "")

    def search(self, hotel: HotelInfo) -> List[PhotoMetadata]:
        if not self.api_key:
            return []

        # 1. Find place by Text Search (name + city)
        place_id = self._find_place(hotel)
        if not place_id:
            return []

        # 2. Get place details including photo references
        photos = self._fetch_place_photos(place_id, hotel)
        return photos

    def _find_place(self, hotel: HotelInfo) -> Optional[str]:
        # Build query: hotel name + city + country
        query_parts = [hotel.name, hotel.city, hotel.country]
        if hotel.address:
            query_parts.append(hotel.address)
        query = quote(", ".join(p for p in query_parts if p))

        url = f"{self.BASE}/textsearch/json?query={query}&key={self.api_key}"
        data = self._fetch_json(url)
        if not data:
            return None

        results = data.get("results", [])
        if not results:
            return None

        # Score results by name/city/address match
        best = None
        best_score = 0.0
        nl = hotel.normalized_name()
        nc = hotel.normalized_city()

        for r in results:
            rn = (r.get("name") or "").lower().strip()
            ra = (r.get("formatted_address") or "").lower().strip()
            score = 0.0
            # Name match (up to 0.5)
            if rn == nl:
                score += 0.5
            elif nl in rn or rn in nl:
                score += 0.3
            else:
                rn_parts = set(rn.split())
                nl_parts = set(nl.split())
                if nl_parts and rn_parts:
                    score += 0.2 * (len(nl_parts & rn_parts) / max(len(nl_parts), len(rn_parts)))
            # City in address (up to 0.2)
            if nc and nc in ra:
                score += 0.2
            # Coordinates bonus (up to 0.1)
            if hotel.lat and hotel.lon:
                gl = r.get("geometry", {}).get("location", {})
                if gl:
                    dlat = abs(gl.get("lat", 0) - hotel.lat)
                    dlng = abs(gl.get("lng", 0) - hotel.lon)
                    if dlat < 0.05 and dlng < 0.05:
                        score += 0.1
            if score > best_score:
                best_score = score
                best = r

        if best and best_score >= 0.4:
            return best.get("place_id")
        return None

    def _fetch_place_photos(self, place_id: str, hotel: HotelInfo) -> List[PhotoMetadata]:
        url = (f"{self.BASE}/details/json?place_id={place_id}"
               f"&fields=name,photos,formatted_address,url"
               f"&key={self.api_key}")
        data = self._fetch_json(url)
        if not data:
            return []

        result = data.get("result", {})
        photos_data = result.get("photos", [])
        if not photos_data:
            return []

        source_url = result.get("url", f"https://maps.google.com/?cid={place_id}")
        photos = []
        for i, p in enumerate(photos_data[:5]):
            photo_ref = p.get("photo_reference", "")
            if not photo_ref:
                continue
            img_url = (f"{self.BASE}/photo?maxwidth=1200"
                       f"&photo_reference={photo_ref}&key={self.api_key}")
            width = p.get("width")
            height = p.get("height")
            photos.append(PhotoMetadata(
                image_url=img_url,
                hotel_name=hotel.name,
                city=hotel.city,
                country=hotel.country,
                provider=self.provider_name,
                provider_hotel_id=place_id,
                source_page_url=source_url,
                attribution="Google Places",
                width=width,
                height=height,
                verification_score=0.0,
                verified=False,
                alt_text=f"{hotel.name} — photo {i + 1}",
                caption=f"{hotel.name}",
            ))
        return photos
