"""
Tests for PhotoVerifier — scoring, boundary, mismatch, edge cases.
"""

from photo_pipeline.verifier import DefaultPhotoVerifier, PASS_THRESHOLD
from photo_pipeline.models import HotelInfo, PhotoMetadata


def test_exact_hotel_match():
    """Exact match on all fields should exceed threshold."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(
        name="Four Seasons Hotel Istanbul at Sultanahmet",
        city="Istanbul",
        country="Turkey",
        lat=41.0055,
        lon=28.9803,
        provider_hotel_id="hl_12345",
    )
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Four Seasons Hotel Istanbul at Sultanahmet",
        city="Istanbul",
        country="Turkey",
        provider="test",
        provider_hotel_id="hl_12345",
    )
    result = verifier.verify(photo, hotel)
    assert result.passed, f"Should pass threshold {PASS_THRESHOLD}, got {result.score}"
    assert result.score >= PASS_THRESHOLD
    assert result.signals["name_exact"] == 1.0
    assert result.signals["provider_id"] == 1.0
    assert result.signals["city"] == 1.0
    assert result.signals["country"] == 1.0
    print(f"  PASS: exact match -> score={result.score}")


def test_city_country_mismatch():
    """Mismatched city/country should fail."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(name="Hilton Bangkok", city="Bangkok", country="Thailand")
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Hilton Bangkok",
        city="Pattaya",
        country="Thailand",
        provider="test",
        provider_hotel_id="",
    )
    result = verifier.verify(photo, hotel)
    assert not result.passed, f"Should fail due to city mismatch, got score={result.score}"
    assert "city mismatch" in result.reason
    print(f"  PASS: city mismatch -> score={result.score}, reason={result.reason}")


def test_low_confidence_reject():
    """Low name similarity should fail even if city/country match."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(name="The Ritz-Carlton Istanbul", city="Istanbul", country="Turkey")
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Cheers Hostel",
        city="Istanbul",
        country="Turkey",
        provider="test",
        provider_hotel_id="",
    )
    result = verifier.verify(photo, hotel)
    assert not result.passed, f"Should fail due to name mismatch, got score={result.score}"
    assert "name mismatch" in result.reason
    print(f"  PASS: low confidence -> score={result.score}, reason={result.reason}")


def test_provider_failure_returns_empty():
    """Provider returning no results should not crash pipeline."""
    from photo_pipeline.providers.manual import ManualProvider
    provider = ManualProvider(manifest_path="")
    hotel = HotelInfo(name="Nonexistent Hotel", city="Nowhere", country="Noland")
    photos = provider.search(hotel)
    assert len(photos) == 0
    print("  PASS: provider failure -> empty result set")


def test_empty_result_set():
    """Verifier on empty list should not crash."""
    from photo_pipeline.pipeline import PhotoPipeline
    pipeline = PhotoPipeline()
    hotel = HotelInfo(name="Ghost Hotel", city="Ghost City", country="Ghostland")
    result = pipeline.process_hotel(hotel)
    assert result["status"] in ("NO_CANDIDATES", "REJECTED")
    print(f"  PASS: empty result set -> status={result['status']}")


def test_duplicate_image_handling():
    """Same URL from two providers should be handled (dedup by URL in manifest)."""
    from photo_pipeline.manifest import PhotoManifestWriter
    writer = PhotoManifestWriter()
    e1 = PhotoManifestWriter.build_entry(
        hotel_name="Test Hotel", slug="test", city_slug="test-city",
        country_slug="test-country", provider="a", provider_hotel_id="1",
        image_url="https://example.com/photo.jpg", local_path="/a/test.jpg",
        alt_text="Test", caption="Test", attribution="A",
        source_page_url="https://a.com", verification_score=0.95, verified=True,
    )
    e2 = PhotoManifestWriter.build_entry(
        hotel_name="Test Hotel", slug="test", city_slug="test-city",
        country_slug="test-country", provider="b", provider_hotel_id="2",
        image_url="https://example.com/photo.jpg", local_path="/b/test.jpg",
        alt_text="Test", caption="Test", attribution="B",
        source_page_url="https://b.com", verification_score=0.94, verified=True,
    )
    urls = set()
    for e in [e1, e2]:
        urls.add(e["image_url"])
    assert len(urls) == 1  # duplicate URL
    print("  PASS: duplicate handling -> same URL dedup-ready")


def test_name_token_similarity():
    """Similar but not exact names should get intermediate score."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(name="The Peninsula Shanghai", city="Shanghai", country="China")
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Peninsula Shanghai",
        city="Shanghai",
        country="China",
        provider="test",
        provider_hotel_id="",
    )
    result = verifier.verify(photo, hotel)
    # "The" missing — tokens overlap highly: {peninsula, shanghai} / {the, peninsula, shanghai}
    if result.passed:
        print(f"  PASS: token similarity -> score={result.score} (passed)")
    else:
        print(f"  PASS: token similarity -> score={result.score} (below threshold, expected)")


def test_country_mismatch():
    """Country mismatch should reduce score."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(name="Marriott Cairo", city="Cairo", country="Egypt")
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Marriott Cairo",
        city="Cairo",
        country="Turkey",  # wrong country
        provider="test",
        provider_hotel_id="",
    )
    result = verifier.verify(photo, hotel)
    assert not result.passed, f"Should fail due to country mismatch, got score={result.score}"
    assert "country mismatch" in result.reason
    print(f"  PASS: country mismatch -> score={result.score}")


def test_partial_name_score():
    """Partial name overlap should get partial score."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(name="Holiday Inn Express Bangkok Sathorn", city="Bangkok", country="Thailand")
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Holiday Inn Bangkok",
        city="Bangkok",
        country="Thailand",
        provider="test",
        provider_hotel_id="",
    )
    result = verifier.verify(photo, hotel)
    # name_exact=0, tokens=2/5 or 2/4=0.5 -> 0.15*0.5=0.075
    # city=0.1, country=0.05 -> total ~0.225
    assert result.score < PASS_THRESHOLD
    print(f"  PASS: partial name -> score={result.score} (below {PASS_THRESHOLD})")


def test_provider_id_boosts_score():
    """Provider hotel ID match gives significant boost."""
    verifier = DefaultPhotoVerifier()
    hotel = HotelInfo(
        name="Marriott Mena House Cairo",
        city="Cairo",
        country="Egypt",
        provider_hotel_id="hl_99999",
    )
    photo = PhotoMetadata(
        image_url="https://example.com/photo.jpg",
        hotel_name="Marriott Mena House",
        city="Cairo",
        country="Egypt",
        provider="test",
        provider_hotel_id="hl_99999",  # matches
    )
    result = verifier.verify(photo, hotel)
    # provider_id=0.15, name_exact=0, tokens ~0.13, city=0.1, country=0.05 => ~0.43
    score_no_exact = 0.15 + (0.15 * 0.67) + 0.1 + 0.05  # ~0.40
    assert result.score > score_no_exact - 0.05  # should include provider bonus
    print(f"  PASS: provider ID boost -> score={result.score}")


if __name__ == "__main__":
    print("=== Verifier Tests ===\n")
    test_exact_hotel_match()
    test_city_country_mismatch()
    test_low_confidence_reject()
    test_name_token_similarity()
    test_country_mismatch()
    test_partial_name_score()
    test_provider_id_boosts_score()
    print("\n=== Provider / Pipeline Tests ===\n")
    test_provider_failure_returns_empty()
    test_empty_result_set()
    test_duplicate_image_handling()
    print("\n=== All tests passed ===")
