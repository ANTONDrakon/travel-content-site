
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
            const url = bg.match(/url\(['"]?([^'")]+)['"]?\)/);
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
