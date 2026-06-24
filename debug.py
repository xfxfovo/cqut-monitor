import os
os.environ["NO_PROXY"] = "*"
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()

    urls = [
        ("教务处", "https://jwc.cqut.edu.cn/index.htm"),
        ("学校主页", "https://www.cqut.edu.cn"),
        ("机械工程学院", "https://jxgcxy.cqut.edu.cn"),
    ]

    for name, url in urls:
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(10000)

            # Get raw bytes and decode properly
            content_bytes = page.evaluate("() => new Response(document.documentElement.outerHTML).arrayBuffer()")
            import codecs
            html = page.content()

            soup = BeautifulSoup(html, "lxml")
            print(f"\n=== {name} ({url}) ===")
            print(f"URL: {page.url}")

            info_links = []
            for a in soup.find_all("a"):
                href = a.get("href", "")
                if "info/" in href or "list" in href or "article" in href or "content" in href:
                    text = a.get_text(strip=True)
                    if text and len(text) > 5:
                        full_url = urljoin(page.url, href)
                        info_links.append((text, full_url))

            if info_links:
                for text, href in info_links[:15]:
                    print(f"  {text[:80]} -> {href[:80]}")
            else:
                print("  No info links found")
        except Exception as e:
            print(f"  ERROR: {e}")

    browser.close()
