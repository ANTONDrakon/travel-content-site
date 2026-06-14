"""
Photo Pipeline — verified hotel photo ingestion system.

Each photo is traced to a concrete hotel via provider-backed property ID.
Photos below 0.93 verification score are rejected.
"""

from photo_pipeline.models import HotelInfo, PhotoMetadata, VerificationResult
from photo_pipeline.interfaces import PhotoProvider, PhotoVerifier, PhotoDownloader, PhotoUploader, PhotoManifestWriter
from photo_pipeline.pipeline import PhotoPipeline

__all__ = [
    "HotelInfo",
    "PhotoMetadata",
    "VerificationResult",
    "PhotoProvider",
    "PhotoVerifier",
    "PhotoDownloader",
    "PhotoUploader",
    "PhotoManifestWriter",
    "PhotoPipeline",
]
