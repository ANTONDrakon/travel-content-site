"""
Manual/Manifest provider.

Reads a user-provided JSON file with pre-verified photo URLs.
This is the highest-trust source — photos here are marked with score=1.0.

Expected format:
[
  {
    "hotel_name": "...",
    "city": "...",
    "country": "...",
    "image_url": "...",
    "source_page_url": "...",
    "attribution": "...",
    "width": 800,
    "height": 600
  }
]
"""

import json
from pathlib import Path
from typing import List

from photo_pipeline.interfaces import PhotoProvider
from photo_pipeline.models import HotelInfo, PhotoMetadata


class ManualProvider(PhotoProvider):

    provider_name = "manual"

    def __init__(self, manifest_path: str = "data/verified_photos.json"):
        self.manifest_path = Path(manifest_path) if manifest_path else None
        self._entries = self._load()

    def _load(self) -> List[dict]:
        if self.manifest_path and self.manifest_path.exists():
            return json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return []

    def search(self, hotel: HotelInfo) -> List[PhotoMetadata]:
        nl = hotel.normalized_name()
        nc = hotel.normalized_city()
        result = []
        for entry in self._entries:
            en = (entry.get("hotel_name") or "").lower().strip()
            ec = (entry.get("city") or "").lower().strip()
            if en == nl and ec == nc:
                result.append(PhotoMetadata(
                    image_url=entry["image_url"],
                    hotel_name=hotel.name,
                    city=hotel.city,
                    country=hotel.country,
                    provider=self.provider_name,
                    provider_hotel_id=entry.get("provider_hotel_id", "manual"),
                    source_page_url=entry.get("source_page_url", ""),
                    attribution=entry.get("attribution", ""),
                    width=entry.get("width"),
                    height=entry.get("height"),
                    verification_score=1.0,
                    verified=True,
                    alt_text=f"{hotel.name} — photo",
                    caption=f"{hotel.name}",
                ))
        return result
