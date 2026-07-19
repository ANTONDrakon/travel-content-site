import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
sys.path.insert(0, str(BASE_DIR))

from config.destinations import DESTINATIONS
from config.prompts import PROMPTS, CONTENT_TYPES
from config.affiliates import hotels_link, flights_link, tours_link, insurance_link
from agents.content_writer import write_article_with_retry
from agents.affiliate_matcher import process_article_body


def build_prompt(content_type, lang, city, country, destination):
    from agents.fact_checker import KNOWN_FACTS
    from config.prompts import CONTENT_TYPES

    airports = ", ".join(city.get("airport_codes", ["N/A"]))
    visa_info = destination["visa_en"] if lang == "en" else destination["visa_ru"]

    # Get currency and timezone from fact checker data
    country_slug = destination.get("slug", country)
    facts = KNOWN_FACTS.get(country_slug, {})
    currency = facts.get("currency", {})
    currency_info = f"{currency.get('name_ru', 'местная валюта')} ({currency.get('code', '')}), символ {currency.get('symbol', '')}" if lang == "ru" else f"{currency.get('name_en', 'local currency')} ({currency.get('code', '')}), symbol {currency.get('symbol', '')}"
    timezone_info = facts.get("timezone", "UTC")

    # Get content type name for context
    ct_info = CONTENT_TYPES.get(content_type, {})
    ct_name = ct_info.get("category_ru" if lang == "ru" else "category_en", content_type)

    prompt = PROMPTS[content_type][lang].format(
        city_name=city["name_en"] if lang == "en" else city["name_ru"],
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
    return prompt


def save_article(country_slug, city_slug, content_type, lang, article_data):
    from agents.seo_optimizer import get_url_slug

    content_slug = get_url_slug(content_type, city_slug, lang)
    out_dir = CONTENT_DIR / lang / country_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{content_slug}.json"

    if out_path.exists():
        print(f"  Skip (exists): {out_path.name}")
        return out_path

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)

    print(f"  Saved: {out_path}")
    return out_path


def generate_article(country_slug, city_slug, content_type, lang):
    destination = DESTINATIONS.get(country_slug)
    if not destination:
        print(f"  Unknown country: {country_slug}")
        return None

    city = destination["cities"].get(city_slug)
    if not city:
        print(f"  Unknown city: {city_slug}")
        return None

    city_name_en = city["name_en"]
    city_name_ru = city["name_ru"]

    print(f"  Generating: {city_name_ru if lang == 'ru' else city_name_en} / {content_type} [{lang}]")

    prompt = build_prompt(content_type, lang, city, destination, destination)
    meta = write_article_with_retry(prompt)

    if not meta or not meta.get("body"):
        print(f"  ERROR: Empty response for {city_slug}/{content_type}/{lang}")
        return None

    body = process_article_body(meta["body"], city_name_en, lang)

    article_data = {
        "title": meta.get("title", ""),
        "meta_description": meta.get("meta_description", ""),
        "h1": meta.get("h1", ""),
        "body": body,
        "country": country_slug,
        "city": city_slug,
        "content_type": content_type,
        "lang": lang,
    }

    save_article(country_slug, city_slug, content_type, lang, article_data)
    return article_data


def generate_city(country_slug, city_slug, langs):
    for lang in langs:
        for ct_slug in CONTENT_TYPES:
            generate_article(country_slug, city_slug, ct_slug, lang)


def generate_country(country_slug, langs):
    destination = DESTINATIONS.get(country_slug)
    if not destination:
        print(f"Unknown country: {country_slug}")
        return

    print(f"\n{'='*60}")
    print(f"Country: {destination['name_ru']} / {destination['name_en']}")
    print(f"Cities: {len(destination['cities'])}")
    print(f"{'='*60}")

    for city_slug in destination["cities"]:
        generate_city(country_slug, city_slug, langs)


def generate_all(langs):
    for country_slug in DESTINATIONS:
        generate_country(country_slug, langs)


def build_site():
    from publisher import build_all
    build_all()
    from sitemap_generator import build_all_sitemaps
    build_all_sitemaps()

    # Generate RSS feeds
    print("\nGenerating RSS feeds...")
    try:
        from rss_generator import build_all_feeds
        build_all_feeds()
    except Exception as e:
        print(f"  Warning: RSS generation failed: {e}")

    # Generate seasonal pages
    print("\nGenerating seasonal pages...")
    try:
        from seasonal_generator import build_all_seasonal
        build_all_seasonal()
    except Exception as e:
        print(f"  Warning: Seasonal pages generation failed: {e}")

    # Generate comparison pages
    print("\nGenerating comparison pages...")
    try:
        from comparison_generator import build_all_comparisons
        build_all_comparisons()
    except Exception as e:
        print(f"  Warning: Comparison pages generation failed: {e}")

    # Optimize images
    print("\nOptimizing images...")
    try:
        from optimize_images import main as optimize_main
        optimize_main()
    except Exception as e:
        print(f"  Warning: Image optimization failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI Travel Content Factory 2.0")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Generate content with AI (legacy pipeline)")
    gen.add_argument("--country", type=str, help="Country slug (e.g. turkey)")
    gen.add_argument("--city", type=str, help="City slug (e.g. istanbul)")
    gen.add_argument("--lang", type=str, default="both", choices=["ru", "en", "both"])
    gen.add_argument("--type", type=str, help="Content type (guide, hotels, flights, attractions, seasons)")

    pipe = sub.add_parser("pipeline", help="Generate with full 12-agent pipeline")
    pipe.add_argument("--country", type=str, help="Country slug")
    pipe.add_argument("--city", type=str, help="City slug")
    pipe.add_argument("--type", type=str, help="Content type")
    pipe.add_argument("--lang", type=str, default="both", choices=["ru", "en", "both"])
    pipe.add_argument("--force", action="store_true", help="Regenerate even if file exists")

    sub.add_parser("build", help="Build static site + sitemaps")

    sub.add_parser("all", help="Generate all content + build site")

    sub.add_parser("analyze", help="Analyze project state and content gaps")

    plan_p = sub.add_parser("plan", help="Content architecture planning")
    plan_p.add_argument("--country", type=str, help="Country slug to plan for")

    qa_p = sub.add_parser("qa", help="Run QA checks on existing content")
    qa_p.add_argument("--agent", type=str, choices=["fact", "seo", "ux", "links", "images", "all"], default="all")

    ls = sub.add_parser("list", help="List available destinations")

    args = parser.parse_args()

    if args.command == "list":
        print("\nAvailable destinations:\n")
        for slug, dest in DESTINATIONS.items():
            print(f"  {slug} — {dest['name_ru']} / {dest['name_en']}")
            for cslug, city in dest["cities"].items():
                print(f"    {cslug} — {city['name_ru']} / {city['name_en']}")
        return

    elif args.command == "generate":
        langs = ["ru", "en"] if args.lang == "both" else [args.lang]

        if args.city and args.type:
            generate_article(args.country, args.city, args.type, langs[0])
            if len(langs) > 1:
                generate_article(args.country, args.city, args.type, langs[1])
        elif args.city:
            generate_city(args.country, args.city, langs)
        elif args.country:
            generate_country(args.country, langs)
        else:
            generate_all(langs)

    elif args.command == "pipeline":
        from agents.pipeline import run_pipeline, run_country_pipeline
        langs = ["ru", "en"] if args.lang == "both" else [args.lang]

        if args.city and args.type:
            for lang in langs:
                result = run_pipeline(args.country, args.city, args.type, lang, force=args.force)
                result.report()
        elif args.country:
            run_country_pipeline(args.country, langs, force=args.force)
        else:
            print("Error: --country is required for pipeline command")
            sys.exit(1)

    elif args.command == "build":
        build_site()

    elif args.command == "all":
        generate_all(["ru", "en"])
        build_site()

    elif args.command == "analyze":
        from agents.project_analyzer import generate_report
        generate_report()

    elif args.command == "plan":
        from agents.content_architect import generate_report
        generate_report(args.country)

    elif args.command == "qa":
        if args.agent == "fact" or args.agent == "all":
            from agents.fact_checker import run as fact_run
            fact_run()
        if args.agent == "seo" or args.agent == "all":
            from agents.copy_seo_agent import run as seo_run
            seo_run()
        if args.agent == "ux" or args.agent == "all":
            from agents.ux_copywriter import run as ux_run
            ux_run()
        if args.agent == "links" or args.agent == "all":
            from agents.link_agent import run as link_run
            link_run()
        if args.agent == "images" or args.agent == "all":
            from agents.image_agent import run as image_run
            image_run()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
