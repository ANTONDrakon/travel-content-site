"""
PhotoDownloader — download images to local staging area.
Converts to WebP with configurable quality.
"""

import hashlib
import io
import time
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

from PIL import Image

from photo_pipeline.interfaces import PhotoDownloader
from photo_pipeline.models import PhotoMetadata

USER_AGENT = "TravelHubPhotoPipeline/2.0"
RETRY_COUNT = 3
RETRY_DELAY = 1.0
MIN_SIZE = 2000


class DefaultPhotoDownloader(PhotoDownloader):

    def __init__(self, quality: int = 88, max_dimension: int = 1200):
        self.quality = quality
        self.max_dimension = max_dimension

    def download(self, photo: PhotoMetadata, target_dir: Path) -> Optional[Path]:
        safe = self._safe_name(photo)
        webp_path = target_dir / f"{safe}.webp"

        if webp_path.exists() and webp_path.stat().st_size > MIN_SIZE:
            return webp_path

        data = self._fetch_with_retry(photo.image_url)
        if not data or len(data) < MIN_SIZE:
            return None

        local = self._convert_to_webp(data, webp_path)
        return local

    def _fetch_with_retry(self, url: str) -> Optional[bytes]:
        for attempt in range(1, RETRY_COUNT + 1):
            try:
                req = Request(url, headers={"User-Agent": USER_AGENT})
                resp = urlopen(req, timeout=30)
                return resp.read()
            except (URLError, OSError):
                if attempt < RETRY_COUNT:
                    time.sleep(RETRY_DELAY)
        return None

    def _convert_to_webp(self, data: bytes, output_path: Path) -> Optional[Path]:
        try:
            img = Image.open(io.BytesIO(data))
            if img.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode in ("RGBA", "LA"):
                    bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else img)
                else:
                    bg.paste(img.convert("RGBA"))
                img = bg
            elif img.mode != "RGB":
                img = img.convert("RGB")
            if img.width > self.max_dimension:
                ratio = self.max_dimension / img.width
                img = img.resize(
                    (self.max_dimension, int(img.height * ratio)), Image.LANCZOS
                )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, format="WEBP", quality=self.quality, method=6)
            return output_path if output_path.exists() else None
        except Exception:
            return None

    def _safe_name(self, photo: PhotoMetadata) -> str:
        raw = f"{photo.provider}|{photo.provider_hotel_id}|{photo.hotel_name}|{photo.image_url}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
