"""
AGENT 12 — Master Pipeline Orchestrator
Runs the full 12-agent pipeline for content generation with gate checks and retry logic.
"""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
MAX_RETRIES = 2


class PipelineResult:
    def __init__(self):
        self.steps = []
        self.passed = True
        self.issues = []

    def add_step(self, name, passed, issues=None, data=None):
        self.steps.append({
            "name": name,
            "passed": passed,
            "issues": issues or [],
            "data": data,
        })
        if not passed:
            self.passed = False
            self.issues.extend(issues or [])

    def report(self):
        print("\n" + "=" * 60)
        print("PIPELINE REPORT")
        print("=" * 60)
        for step in self.steps:
            status = "✓ PASS" if step["passed"] else "✗ FAIL"
            print(f"  {status} — {step['name']}")
            for issue in step.get("issues", []):
                print(f"         {issue}")
        print(f"\n  Overall: {'PASSED' if self.passed else 'FAILED'}")
        return self.passed


def run_pipeline(country_slug, city_slug, content_type, lang, force=False):
    """Run the full 12-agent pipeline for a single article."""
    result = PipelineResult()

    # Check if file already exists
    from agents.seo_optimizer import get_url_slug
    content_slug = get_url_slug(content_type, city_slug, lang)
    out_path = CONTENT_DIR / lang / country_slug / f"{content_slug}.json"

    if out_path.exists() and not force:
        print(f"  Skip (exists): {out_path.name}")
        result.add_step("Skip", True, data={"reason": "File already exists"})
        return result

    retries = 0
    while retries <= MAX_RETRIES:
        result = PipelineResult()
        article_data = None

        # Step 1: Travel Writer — generate draft
        print(f"\n[Step 1] Travel Writer — generating draft...")
        try:
            from agents.content_writer import write_article_with_retry
            from config.destinations import DESTINATIONS
            from config.prompts import PROMPTS, CONTENT_TYPES

            destination = DESTINATIONS.get(country_slug)
            if not destination:
                result.add_step("Travel Writer", False, [f"Unknown country: {country_slug}"])
                return result

            city = destination["cities"].get(city_slug)
            if not city:
                result.add_step("Travel Writer", False, [f"Unknown city: {city_slug}"])
                return result

            # Build prompt
            from agents.fact_checker import KNOWN_FACTS
            airports = ", ".join(city.get("airport_codes", ["N/A"]))
            visa_info = destination["visa_en"] if lang == "en" else destination["visa_ru"]
            city_name = city["name_en"] if lang == "en" else city["name_ru"]

            # Get currency and timezone from fact checker data
            facts = KNOWN_FACTS.get(country_slug, {})
            currency = facts.get("currency", {})
            currency_info = f"{currency.get('name_ru', 'местная валюта')} ({currency.get('code', '')}), символ {currency.get('symbol', '')}" if lang == "ru" else f"{currency.get('name_en', 'local currency')} ({currency.get('code', '')}), symbol {currency.get('symbol', '')}"
            timezone_info = facts.get("timezone", "UTC")

            prompt = PROMPTS[content_type][lang].format(
                city_name=city_name,
                country_name=destination["name_en"] if lang == "en" else destination["name_ru"],
                airports=airports,
                visa_info=visa_info,
                currency_info=currency_info,
                timezone_info=timezone_info,
                hotels_placeholder="{hotels_placeholder}",
                flights_placeholder="{flights_placeholder}",
                tours_placeholder="{tours_placeholder}",
                excursions_placeholder="{excursions_placeholder}",
                transfers_placeholder="{transfers_placeholder}",
                esim_placeholder="{esim_placeholder}",
                car_rental_placeholder="{car_rental_placeholder}",
                insurance_placeholder="{insurance_placeholder}",
                tickets_placeholder="{tickets_placeholder}",
            )

            meta = write_article_with_retry(prompt)
            if not meta or not meta.get("body"):
                result.add_step("Travel Writer", False, ["Empty response from AI"])
                retries += 1
                continue

            article_data = {
                "title": meta.get("title", ""),
                "meta_description": meta.get("meta_description", ""),
                "h1": meta.get("h1", ""),
                "body": meta["body"],
                "country": country_slug,
                "city": city_slug,
                "content_type": content_type,
                "lang": lang,
            }
            result.add_step("Travel Writer", True, data={"words": len(meta["body"].split())})

        except Exception as e:
            result.add_step("Travel Writer", False, [str(e)])
            retries += 1
            continue

        # Step 2: Fact Checker — verify claims
        print(f"[Step 2] Fact Checker — verifying claims...")
        from agents.fact_checker import check_article
        fact_issues = check_article(article_data["body"], country_slug, lang)
        if fact_issues:
            result.add_step("Fact Checker", False, fact_issues)
            # If critical issues, retry
            critical = [i for i in fact_issues if i.startswith("UNVERIFIED") or i.startswith("MISSING")]
            if critical and retries < MAX_RETRIES:
                retries += 1
                continue
        else:
            result.add_step("Fact Checker", True)

        # Step 3: SEO Optimizer — optimize structure
        print(f"[Step 3] SEO Optimizer — optimizing structure...")
        from agents.seo_optimizer import get_url_slug, build_seo_meta
        try:
            seo_meta = build_seo_meta(article_data, city_slug, country_slug, content_type, lang)
            article_data["seo"] = seo_meta
            result.add_step("SEO Optimizer", True)
        except Exception as e:
            result.add_step("SEO Optimizer", False, [str(e)])

        # Step 4: Affiliate Engine — inject affiliate blocks
        print(f"[Step 4] Affiliate Engine — injecting affiliate blocks...")
        from agents.affiliate_matcher import process_article_body
        city_name_en = city["name_en"]
        article_data["body"] = process_article_body(article_data["body"], city_name_en, lang)
        result.add_step("Affiliate Engine", True)

        # Step 5: Internal Link Builder — add cross-links
        print(f"[Step 5] Internal Link Builder — adding cross-links...")
        try:
            from agents.internal_link_builder import build_link_graph, inject_related_section
            graph = build_link_graph()
            # Build current article path for graph lookup
            from agents.seo_optimizer import get_url_slug
            content_slug = get_url_slug(content_type, city_slug, lang)
            current_path = f"content/{lang}/{country_slug}/{content_slug}.json"
            related_section = inject_related_section(current_path, graph, lang)
            if related_section:
                article_data["body"] += related_section
            result.add_step("Internal Link Builder", True)
        except Exception as e:
            result.add_step("Internal Link Builder", False, [str(e)])

        # Step 6: UX Copywriter — polish content
        print(f"[Step 6] UX Copywriter — polishing content...")
        from agents.ux_copywriter import remove_ai_fingerprints, validate_structure, check_cta_presence, break_long_paragraphs
        article_data["body"] = remove_ai_fingerprints(article_data["body"], lang)
        article_data["body"] = break_long_paragraphs(article_data["body"], max_chars=500)
        struct_issues = validate_structure(article_data["body"])
        cta_issues = check_cta_presence(article_data["body"], lang)
        all_ux_issues = struct_issues + cta_issues
        if all_ux_issues:
            result.add_step("UX Copywriter", False, all_ux_issues)
        else:
            result.add_step("UX Copywriter", True)

        # Step 7: Save article
        print(f"[Step 7] Saving article...")
        from agents.seo_optimizer import get_url_slug
        content_slug = get_url_slug(content_type, city_slug, lang)
        out_dir = CONTENT_DIR / lang / country_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{content_slug}.json"

        if not out_path.exists():
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(article_data, f, ensure_ascii=False, indent=2)
            print(f"  Saved: {out_path}")
        else:
            print(f"  Exists: {out_path}")

        result.add_step("Save", True)
        break  # Success — exit retry loop

    return result


def run_country_pipeline(country_slug, langs=None, force=False):
    """Run pipeline for all cities in a country."""
    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    if langs is None:
        langs = ["ru", "en"]

    dest = DESTINATIONS.get(country_slug)
    if not dest:
        print(f"Unknown country: {country_slug}")
        return

    results = []
    for city_slug, city_data in dest.get("cities", {}).items():
        for lang in langs:
            for ct_slug in CONTENT_TYPES:
                print(f"\n{'='*60}")
                print(f"Processing: {dest['name_en']}/{city_slug}/{ct_slug}/{lang}")
                print(f"{'='*60}")
                result = run_pipeline(country_slug, city_slug, ct_slug, lang, force=force)
                result.report()
                results.append(result)

    passed = sum(1 for r in results if r.passed)
    print(f"\n{'='*60}")
    print(f"COUNTRY SUMMARY: {passed}/{len(results)} articles passed")
    print(f"{'='*60}")

    return results


def run_all_pipelines(langs=None):
    """Run pipeline for all countries."""
    from config.destinations import DESTINATIONS

    if langs is None:
        langs = ["ru", "en"]

    for country_slug in DESTINATIONS:
        run_country_pipeline(country_slug, langs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m agents.pipeline <country> [city] [content_type] [lang]")
        print("       python -m agents.pipeline --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        run_all_pipelines()
    elif len(sys.argv) >= 2:
        country = sys.argv[1]
        city = sys.argv[2] if len(sys.argv) > 2 else None
        ct = sys.argv[3] if len(sys.argv) > 3 else None
        lang = sys.argv[4] if len(sys.argv) > 4 else "both"

        if city and ct:
            langs = ["ru", "en"] if lang == "both" else [lang]
            for l in langs:
                result = run_pipeline(country, city, ct, l)
                result.report()
        elif city:
            run_country_pipeline(country)
        else:
            run_country_pipeline(country)
