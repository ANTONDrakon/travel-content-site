from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path

from .models import HotelInfo, PhotoMetadata, VerificationResult


class PhotoProvider(ABC):
    """Fetch candidate photos for a hotel from a specific source."""

    @abstractmethod
    def search(self, hotel: HotelInfo) -> List[PhotoMetadata]:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...


class PhotoVerifier(ABC):
    """Confirm that a photo actually depicts the given hotel."""

    @abstractmethod
    def verify(self, photo: PhotoMetadata, hotel: HotelInfo) -> VerificationResult:
        ...


class PhotoDownloader(ABC):
    """Download an image to local storage."""

    @abstractmethod
    def download(self, photo: PhotoMetadata, target_dir: Path) -> Optional[Path]:
        ...


class PhotoUploader(ABC):
    """Upload a local image to site storage / CDN."""

    @abstractmethod
    def upload(self, local_path: Path, remote_key: str) -> str:
        ...


class PhotoManifestWriter(ABC):
    """Persist photo-to-hotel mapping as a JSON manifest."""

    @abstractmethod
    def write(self, entries: List[dict], path: Path):
        ...

    @abstractmethod
    def read(self, path: Path) -> List[dict]:
        ...
