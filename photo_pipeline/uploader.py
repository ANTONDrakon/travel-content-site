"""
PhotoUploader — copies verified photos to the site's asset directory
and returns the public URL path.

Also generates alt text and caption using the exact hotel name.
"""

import shutil
from pathlib import Path
from typing import Optional

from photo_pipeline.interfaces import PhotoUploader
from photo_pipeline.models import PhotoMetadata


class LocalPhotoUploader(PhotoUploader):

    def __init__(self, assets_root: str = "docs/assets/hotels"):
        self.assets_root = Path(assets_root)

    def upload(self, local_path: Path, remote_key: str) -> str:
        dest = self.assets_root / remote_key
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local_path, dest)
        return f"/assets/hotels/{remote_key}"

    @staticmethod
    def generate_alt_text(photo: PhotoMetadata, lang: str = "ru") -> str:
        if lang == "ru":
            return f"{photo.hotel_name} — {photo.city}, {photo.country}. Фото: {photo.attribution}"
        return f"{photo.hotel_name} — {photo.city}, {photo.country}. Photo: {photo.attribution}"

    @staticmethod
    def generate_caption(photo: PhotoMetadata) -> str:
        return photo.hotel_name
