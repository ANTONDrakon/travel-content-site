"""Debug the booking search - step by step."""
import urllib.request, urllib.parse, json, re, ssl, gzip

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def fetch(url, name):
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = resp.read()
        if data[:2] == b'\x1f\x8b':
            data = gzip.decompress(data)
        text = data.decode("utf-8", errors="replace")
        print(f"=== {name}: {len(text)} bytes ===")
        if len(text) < 6000:
            print(f"  SHORT PAGE (likely bot block): {text[:200]}")
        else:
            hid = re.search(r'"hotel_id"\s*:\s*(\d+)', text)
            print(f"  hotel_id: {hid.group(1) if hid else 'NOT FOUND'}")
        return text
    except Exception as e:
        print(f"=== {name}: {type(e).__name__}: {str(e)[:100]} ===")
        return None

# 1. Try direct Booking URL for Holiday Inn Express Dongzhimen, Beijing
fetch("https://www.booking.com/hotel/cn/holiday-inn-express-dongzhimen.html", "direct slug")
fetch("https://www.booking.com/hotel/cn/holiday-inn-express-dongzhimen-beijing.html", "direct slug 2")
fetch("https://www.booking.com/hotel/cn/holiday-inn-express-dongzhi-men.html", "direct slug 3")

# 2. Bing search for Holiday Inn Express Dongzhimen Beijing
search_q = "booking.com Holiday Inn Express Dongzhimen Beijing"
search_url = f"https://www.bing.com/search?q={urllib.parse.quote(search_q)}&count=5"
fetch(search_url, "bing search")

# 3. Bing search with site:booking.com
search_url2 = f"https://www.bing.com/search?q=site:booking.com+%22Holiday+Inn+Express%22+Dongzhimen+Beijing&count=5"
fetch(search_url2, "bing site:booking.com")

# 4. Bing search for just the hotel
search_url3 = f"https://www.bing.com/search?q=%22Holiday+Inn+Express+Dongzhimen%22+Beijing+hotel&count=5"
fetch(search_url3, "bing exact hotel name")
