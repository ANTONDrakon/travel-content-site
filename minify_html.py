"""
HTML Minifier for TravelHub
Reduces HTML file size by removing whitespace, comments, and redundant characters.
"""
import re
import sys
from pathlib import Path


def minify_html(html: str, remove_comments: bool = True) -> str:
    """
    Minify HTML content.
    
    Args:
        html: Raw HTML string
        remove_comments: Whether to remove HTML comments
        
    Returns:
        Minified HTML string
    """
    if not html:
        return html
    
    # Store template tags to preserve them
    template_tags = {}
    counter = [0]
    
    def preserve_template(match):
        key = f"__TMPL{counter[0]}__"
        template_tags[key] = match.group(0)
        counter[0] += 1
        return key
    
    # Preserve Jinja2 template tags
    html = re.sub(r'\{%.*?%\}', preserve_template, html)
    html = re.sub(r'\{\{.*?\}\}', preserve_template, html)
    
    # Remove HTML comments (but not conditional comments)
    if remove_comments:
        html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.DOTALL)
    
    # Remove whitespace between tags
    html = re.sub(r'>\s+<', '> <', html)
    html = re.sub(r'\s+', ' ', html)
    
    # Remove leading/trailing whitespace
    html = html.strip()
    
    # Restore template tags
    for key, value in template_tags.items():
        html = html.replace(key, value)
    
    return html


def minify_css(css: str) -> str:
    """
    Minify CSS content.
    
    Args:
        css: Raw CSS string
        
    Returns:
        Minified CSS string
    """
    if not css:
        return css
    
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)
    css = re.sub(r';}', '}', css)
    
    return css.strip()


def minify_js(js: str) -> str:
    """
    Minify JavaScript content (basic).
    
    Args:
        js: Raw JavaScript string
        
    Returns:
        Minified JavaScript string
    """
    if not js:
        return js
    
    # Remove single-line comments (but not URLs)
    js = re.sub(r'(?<!:)//.*$', '', js, flags=re.MULTILINE)
    
    # Remove multi-line comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    
    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in js.split('\n')]
    lines = [line for line in lines if line]
    
    return '\n'.join(lines)


def minify_file(input_path: Path, output_path: Path = None, file_type: str = 'html') -> dict:
    """
    Minify a single file.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file (defaults to overwriting input)
        file_type: File type ('html', 'css', 'js')
        
    Returns:
        Dict with stats
    """
    if not input_path.exists():
        return {'error': f'File not found: {input_path}'}
    
    original_size = input_path.stat().st_size
    
    # Read file
    content = input_path.read_text(encoding='utf-8')
    
    # Minify based on type
    if file_type == 'html':
        minified = minify_html(content)
    elif file_type == 'css':
        minified = minify_css(content)
    elif file_type == 'js':
        minified = minify_js(content)
    else:
        minified = content
    
    # Write output
    output_path = output_path or input_path
    output_path.write_text(minified, encoding='utf-8')
    
    new_size = len(minified.encode('utf-8'))
    
    return {
        'input': str(input_path),
        'output': str(output_path),
        'original_size': original_size,
        'minified_size': new_size,
        'reduction': round((1 - new_size / original_size) * 100, 1) if original_size > 0 else 0
    }


def minify_directory(directory: Path, file_types: list = None) -> list:
    """
    Minify all files in a directory.
    
    Args:
        directory: Directory to process
        file_types: List of file extensions to minify (default: html, css, js)
        
    Returns:
        List of results
    """
    if file_types is None:
        file_types = ['.html', '.css', '.js']
    
    results = []
    
    for ext in file_types:
        for file_path in directory.rglob(f'*{ext}'):
            # Skip already minified files
            if '.min.' in file_path.name:
                continue
            
            # Skip template files
            if 'templates' in str(file_path):
                continue
            
            result = minify_file(file_path, file_type=ext[1:])
            results.append(result)
    
    return results


def main():
    """CLI interface for HTML minification."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Minify HTML, CSS, and JS files')
    parser.add_argument('path', help='File or directory to minify')
    parser.add_argument('--type', choices=['html', 'css', 'js', 'all'], default='html',
                        help='File type to minify (default: html)')
    parser.add_argument('--output', help='Output file (for single file mode)')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        # Single file mode
        ext = args.type if args.type != 'all' else path.suffix[1:]
        result = minify_file(path, Path(args.output) if args.output else None, ext)
        
        if args.stats:
            print(f"Minified: {result['input']}")
            print(f"  Original: {result['original_size']:,} bytes")
            print(f"  Minified: {result['minified_size']:,} bytes")
            print(f"  Reduction: {result['reduction']}%")
    
    elif path.is_dir():
        # Directory mode
        file_types = ['.html', '.css', '.js'] if args.type == 'all' else [f'.{args.type}']
        results = minify_directory(path, file_types)
        
        if args.stats:
            total_original = sum(r['original_size'] for r in results)
            total_minified = sum(r['minified_size'] for r in results)
            
            print(f"\nMinification complete:")
            print(f"  Files processed: {len(results)}")
            print(f"  Original total: {total_original:,} bytes")
            print(f"  Minified total: {total_minified:,} bytes")
            print(f"  Total reduction: {round((1 - total_minified / total_original) * 100, 1) if total_original > 0 else 0}%")
    
    else:
        print(f"Error: {path} is not a file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
