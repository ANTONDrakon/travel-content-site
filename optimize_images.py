"""
Image Optimization Script for TravelHub
Converts images to WebP, compresses, and generates responsive sizes.
"""
import os
import sys
import json
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "optimized"

# Quality settings
WEBP_QUALITY = 80
JPEG_QUALITY = 85
MAX_WIDTH = 1200
MAX_HEIGHT = 800

# Responsive sizes
RESPONSIVE_SIZES = {
    "hero": [(1600, 900), (1200, 675), (800, 450)],
    "card": [(800, 450), (600, 340), (400, 225)],
    "avatar": [(200, 200), (100, 100), (50, 50)],
}


def ensure_dirs():
    """Create necessary directories."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def optimize_image(input_path, output_path, max_size=None, quality=None, format="WEBP"):
    """Optimize a single image."""
    try:
        # Check if file exists and has content
        if not input_path.exists() or input_path.stat().st_size == 0:
            return False
        
        # Check file extension
        ext = input_path.suffix.lower()
        if ext not in (".webp", ".jpg", ".jpeg", ".png", ".gif", ".bmp"):
            return False
        
        img = Image.open(input_path)
        
        # Auto-orient based on EXIF
        img = ImageOps.exif_transpose(img)
        
        # Convert to RGB if necessary (for WebP/JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Resize if needed
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save
        if format.upper() == "WEBP":
            img.save(output_path, "WEBP", quality=quality or WEBP_QUALITY, method=6)
        elif format.upper() == "JPEG":
            img.save(output_path, "JPEG", quality=quality or JPEG_QUALITY, optimize=True)
        else:
            img.save(output_path)
        
        return True
    except Exception as e:
        # Silently skip corrupted files
        return False


def get_file_size(path):
    """Get file size in KB."""
    return os.path.getsize(path) / 1024


def optimize_url_image(url, output_name, size_type="card"):
    """Download and optimize an image from URL."""
    import urllib.request
    
    output_path = IMAGES_DIR / f"{output_name}.webp"
    
    if output_path.exists():
        return output_path
    
    try:
        # Add optimization params to Unsplash URLs
        if "unsplash.com" in url:
            # Request optimized version
            base_url = url.split("?")[0]
            url = f"{base_url}?w=800&q=75&fm=webp"
        
        req = urllib.request.Request(url, headers={"User-Agent": "TravelHub/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            
            # Save temp file
            temp_path = IMAGES_DIR / f"temp_{output_name}"
            temp_path.write_bytes(data)
            
            # Optimize
            max_size = RESPONSIVE_SIZES.get(size_type, [(800, 450)])[0]
            optimize_image(temp_path, output_path, max_size=max_size)
            
            # Remove temp
            temp_path.unlink()
            
            return output_path
    except Exception as e:
        print(f"  Could not download {url}: {e}")
        return None


def generate_responsive_set(input_path, output_name, size_type="card"):
    """Generate multiple sizes for responsive images."""
    sizes = RESPONSIVE_SIZES.get(size_type, [(800, 450)])
    results = []
    
    for width, height in sizes:
        suffix = f"_{width}w"
        output_path = IMAGES_DIR / f"{output_name}{suffix}.webp"
        
        if not output_path.exists():
            optimize_image(input_path, output_path, max_size=(width, height))
        
        size_kb = get_file_size(output_path) if output_path.exists() else 0
        results.append({
            "width": width,
            "path": str(output_path.relative_to(DOCS_DIR)),
            "size_kb": round(size_kb, 1)
        })
    
    return results


def create_responsive_css():
    """Create CSS for responsive images with lazy loading."""
    css = """
/* Responsive image loading */
img[loading="lazy"] {
    opacity: 0;
    transition: opacity 0.3s ease-in;
}
img[loading="lazy"].loaded,
img[loading="lazy"]:not([data-src]) {
    opacity: 1;
}

/* Image placeholder gradient */
img {
    background: linear-gradient(135deg, #e8e0d6 0%, #f8f5f0 100%);
    min-height: 100px;
}

/* Hero background optimization */
.hero-section {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
"""
    
    output_path = ASSETS_DIR / "styles.css"
    
    # Read existing styles
    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")
        # Check if responsive styles already exist
        if "img[loading=" in existing:
            return
        existing += css
        output_path.write_text(existing, encoding="utf-8")
    else:
        output_path.write_text(css, encoding="utf-8")
    
    print("  Created responsive image CSS")


def create_lazy_loading_js():
    """Create JavaScript for lazy loading images."""
    js = """
// Lazy loading with Intersection Observer
document.addEventListener('DOMContentLoaded', function() {
    // Lazy load images
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                    }
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '100px'  // Start loading 100px before visible
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    } else {
        // Fallback: just show all images
        lazyImages.forEach(function(img) {
            img.classList.add('loaded');
        });
    }
    
    // Optimize hero background images
    const heroSections = document.querySelectorAll('.hero-section');
    heroSections.forEach(function(hero) {
        const bg = getComputedStyle(hero).backgroundImage;
        if (bg && bg !== 'none') {
            // Add loading class
            hero.style.opacity = '0';
            hero.style.transition = 'opacity 0.5s ease-in';
            
            // Preload the image
            const url = bg.match(/url\\(['\"]?([^'\")]+)['\"]?\\)/);
            if (url && url[1]) {
                const img = new Image();
                img.onload = function() {
                    hero.style.opacity = '1';
                };
                img.src = url[1];
            } else {
                hero.style.opacity = '1';
            }
        }
    });
});
"""
    
    output_path = ASSETS_DIR / "lazy.js"
    output_path.write_text(js, encoding="utf-8")
    print("  Created lazy loading JavaScript")


def main():
    """Main optimization flow."""
    print("\n=== Image Optimization ===\n")
    
    ensure_dirs()
    
    # Create lazy loading assets
    print("Creating lazy loading assets...")
    create_responsive_css()
    create_lazy_loading_js()
    
    # Create image manifest
    manifest = {
        "optimized": [],
        "total_size_kb": 0
    }
    
    # Optimize existing images in docs/assets
    docs_assets = DOCS_DIR / "assets"
    if docs_assets.exists():
        print("\nOptimizing existing images...")
        for img_path in docs_assets.rglob("*.webp"):
            if "optimized" in str(img_path):
                continue
            
            output_name = img_path.stem
            output_path = IMAGES_DIR / f"{output_name}.webp"
            
            if not output_path.exists():
                success = optimize_image(img_path, output_path, max_size=(800, 450))
                if success:
                    size_kb = get_file_size(output_path)
                    manifest["optimized"].append({
                        "original": str(img_path.relative_to(DOCS_DIR)),
                        "optimized": str(output_path.relative_to(DOCS_DIR)),
                        "size_kb": round(size_kb, 1)
                    })
                    manifest["total_size_kb"] += size_kb
                    print(f"  Optimized: {img_path.name} -> {size_kb:.1f}KB")
    
    # Save manifest
    manifest_path = IMAGES_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    
    print(f"\n=== Optimization Complete ===")
    print(f"Total optimized images: {len(manifest['optimized'])}")
    print(f"Total size: {manifest['total_size_kb']:.1f}KB")
    print(f"\nAssets created:")
    print(f"  - assets/optimized/ (optimized images)")
    print(f"  - assets/lazy.js (lazy loading)")
    print(f"  - assets/optimized/manifest.json")


if __name__ == "__main__":
    main()
