"""Add EXIF metadata (hotel name) to all hotel photos for search engines + AI indexing."""
import json, struct, io
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import Base
except ImportError:
    pass

BASE = Path(__file__).parent
HOTELS_DB = BASE / "data" / "hotels.json"
ASSETS = BASE / "docs" / "assets" / "hotels"

hotels = json.loads(HOTELS_DB.read_text(encoding="utf-8"))


def add_metadata(img_path, hotel_name, city, country):
    """Re-save WebP with EXIF metadata (ImageDescription, Artist, Copyright, Software)."""
    try:
        img = Image.open(img_path)

        # Create EXIF-like metadata using piexif-compatible format
        # For WebP, we embed data in XMP or use info dict
        info = img.info or {}

        # Add structured data to image info
        info["exif"] = b""  # Empty exif for WebP

        # Re-save with metadata embedded in the image format
        # WebP supports XMP metadata
        xmp_data = f"""<?xpacket begin="ï»¿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"
    dc:title="{hotel_name} - {city}, {country}"
    dc:description="Photo of {hotel_name} in {city}, {country}. Hotel photo for travel guide."
    dc:subject="{hotel_name},{city},{country},hotel,travel"
    dc:creator="TravelHub"
    dc:rights="TravelHub Travel Guides"
    photoshop:Credit="TravelHub"
    photoshop:City="{city}"
    photoshop:Country="{country}"
    Iptc4xmpCore:CreatorContactInfo="TravelHub">
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""

        # Save with XMP metadata
        img.save(img_path, format="WEBP", quality=82, method=6,
                 exif=b"\x00",  # minimal exif marker
                 xmp=xmp_data.encode("utf-8"))
        return True
    except Exception as e:
        print(f"  Metadata error: {e}")
        return False


def main():
    updated = 0
    for h in hotels:
        hotel_dir = ASSETS / h["country_slug"] / h["city_slug"] / h["slug"]
        if not hotel_dir.exists():
            continue

        photos = sorted(hotel_dir.glob("*.webp"))
        if not photos:
            continue

        for photo in photos:
            try:
                add_metadata(
                    photo,
                    h["name"],
                    h.get("city_name_en", h["city_slug"].replace("-", " ").title()),
                    h["country_slug"].title(),
                )
                updated += 1
            except Exception as e:
                print(f"  Error {photo.name}: {e}")

    print(f"Updated {updated} photos with metadata")


if __name__ == "__main__":
    main()
