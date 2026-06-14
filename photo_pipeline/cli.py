#!/usr/bin/env python3
"""
CLI entry point for the Photo Pipeline.

Usage:
    python -m photo_pipeline.cli process --all
    python -m photo_pipeline.cli process --hotel "Four Seasons Istanbul" --country turkey --city istanbul
    python -m photo_pipeline.cli verify --hotel "Four Seasons Istanbul" --country turkey --city istanbul
    python -m photo_pipeline.cli test
    python -m photo_pipeline.cli report
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))


def cmd_process(args):
    from photo_pipeline.pipeline import PhotoPipeline
    from photo_pipeline.models import HotelInfo

    pipeline = PhotoPipeline()

    if args.all:
        print("Processing all hotels from data/hotels.json...")
        results = pipeline.process_all_hotels()
        return

    if args.hotel and args.country and args.city:
        hotel = HotelInfo(
            name=args.hotel,
            city=args.city.replace("-", " ").title(),
            country=args.country,
            slug=args.hotel.lower().replace(" ", "-"),
        )
        print(f"Processing {hotel.name}...")
        result = pipeline.process_hotel(hotel)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("Specify --all or --hotel + --country + --city")


def cmd_verify(args):
    from photo_pipeline.verifier import DefaultPhotoVerifier
    from photo_pipeline.models import HotelInfo, PhotoMetadata

    hotel = HotelInfo(
        name=args.hotel,
        city=args.city.replace("-", " ").title(),
        country=args.country,
    )
    photo = PhotoMetadata(
        image_url=args.url or "https://example.com/photo.jpg",
        hotel_name=args.hotel,
        city=args.city.replace("-", " ").title(),
        country=args.country,
        provider="cli",
        provider_hotel_id=args.provider_id or "",
        source_page_url=args.source_url or "",
        attribution=args.attribution or "unknown",
    )
    verifier = DefaultPhotoVerifier()
    result = verifier.verify(photo, hotel)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


def cmd_test(args):
    from photo_pipeline.tests import test_verifier as tests

    test_fns = [
        tests.test_exact_hotel_match,
        tests.test_city_country_mismatch,
        tests.test_low_confidence_reject,
        tests.test_provider_failure_returns_empty,
        tests.test_empty_result_set,
        tests.test_duplicate_image_handling,
        tests.test_name_token_similarity,
        tests.test_country_mismatch,
        tests.test_partial_name_score,
        tests.test_provider_id_boosts_score,
    ]
    passed = 0
    failed = 0
    for fn in test_fns:
        name = fn.__name__
        try:
            fn()
            print(f"  OK: {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {name} -> {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


def cmd_report(args):
    from photo_pipeline.pipeline import PhotoPipeline
    pipeline = PhotoPipeline()
    print(json.dumps(pipeline.summary(), indent=2))
    mpath = pipeline.manifest_path
    if mpath.exists():
        entries = pipeline.manifest_writer.read(mpath)
        print(f"\nManifest: {len(entries)} photos")
        verified = sum(1 for e in entries if e.get("verified"))
        print(f"Verified: {verified}, Unverified: {len(entries) - verified}")


def main():
    parser = argparse.ArgumentParser(description="Photo Pipeline CLI")
    sub = parser.add_subparsers(dest="command")

    p_process = sub.add_parser("process", help="Run photo pipeline")
    p_process.add_argument("--all", action="store_true", help="Process all hotels")
    p_process.add_argument("--hotel", type=str, help="Hotel name")
    p_process.add_argument("--country", type=str, help="Country slug")
    p_process.add_argument("--city", type=str, help="City slug")

    p_verify = sub.add_parser("verify", help="Verify a single photo")
    p_verify.add_argument("--hotel", type=str, required=True)
    p_verify.add_argument("--country", type=str, required=True)
    p_verify.add_argument("--city", type=str, required=True)
    p_verify.add_argument("--url", type=str, help="Photo URL")
    p_verify.add_argument("--provider-id", type=str, help="Provider hotel ID")
    p_verify.add_argument("--source-url", type=str, help="Source page URL")
    p_verify.add_argument("--attribution", type=str, help="Attribution text")

    sub.add_parser("test", help="Run verification tests")
    sub.add_parser("report", help="Pipeline summary")

    args = parser.parse_args()
    if args.command == "process":
        cmd_process(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "test":
        sys.exit(cmd_test(args))
    elif args.command == "report":
        cmd_report(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
