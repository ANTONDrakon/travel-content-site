from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class HotelInfo:
    """Canonical hotel identity used for matching and verification."""

    name: str
    city: str
    country: str
    slug: str = ""
    address: str = ""
    lat: Optional[float] = None
    lon: Optional[float] = None
    provider_hotel_id: str = ""
    provider: str = ""

    def normalized_name(self) -> str:
        return self.name.lower().strip()

    def normalized_city(self) -> str:
        return self.city.lower().strip()

    def normalized_country(self) -> str:
        return self.country.lower().strip()


@dataclass
class PhotoMetadata:
    """Every photo carries full provenance so it can be verified independently."""

    image_url: str
    hotel_name: str
    city: str
    country: str
    provider: str
    provider_hotel_id: str
    source_page_url: str = ""
    attribution: str = ""
    width: Optional[int] = None
    height: Optional[int] = None

    verification_score: float = 0.0
    verified: bool = False

    alt_text: str = ""
    caption: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PhotoMetadata":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class VerificationResult:
    """Outcome of verifying a photo against a hotel."""

    photo: PhotoMetadata
    score: float
    passed: bool
    signals: dict = field(default_factory=dict)
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "passed": self.passed,
            "signals": self.signals,
            "reason": self.reason,
            "photo": self.photo.to_dict(),
        }
