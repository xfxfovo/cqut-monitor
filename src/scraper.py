import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
import random
import time

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
]

def generate_id(title, url):
    content = f"{title}:{url}"
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def fetch_page(url, retries=3):
    session = requests.Session()
    for attempt in range(retries):
        try:
            resp = session.get(
                url,
                headers=random.choice(HEADERS_LIST),
                timeout=20,
                verify=False,
                allow_redirects=True,
            )
            if resp.status_code == 200:
                resp.encoding = resp.apparent_encoding or "utf-8"
                return resp.text
            time.sleep(2)
        except Exception as e:
            print(f"    Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None

def parse_notices(html, base_url, site_name):
    notices = []
    soup = BeautifulSoup(html, "lxml")

    selectors = [
        "ul.news-list li",
        "ul.list li",
        "div.news-list li",
        "table.list_table tr",
        "div.list-item",
        "div.list_item",
        "li.list_item",
        "ul.notice-list li",
        "div.notice-list li",
        "div.content li",
        "div.main li",
        "div.right li",
    ]

    items = []
    for sel in selectors:
        items = soup.select(sel)
        if items:
            break

    if not items:
        items = soup.select("a[href]")

    for item in items[:50]:
        try:
            if item.name == "a":
                link_tag = item
            else:
                link_tag = item.select_one("a[href]")

            if not link_tag or not link_tag.get("href"):
                continue

            href = link_tag["href"]
            if href.startswith("javascript") or href == "#" or href == "javascript:void(0)":
                continue

            full_link = urljoin(base_url, href)
            title = link_tag.get_text(strip=True)

            if not title or len(title) < 4 or len(title) > 200:
                continue

            skip_words = ["首页", "关于我们", "联系我们", "登录", "注册", "更多"]
            if any(w in title for w in skip_words):
                continue

            date_tag = item.select_one("span.date, span.time, td:last-child, span:nth-child(2)")
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            notice_id = generate_id(title, full_link)

            notices.append({
                "id": notice_id,
                "title": title,
                "url": full_link,
                "date": date_str,
                "source": site_name,
            })
        except Exception:
            continue

    return notices

def scrape_website(site_config):
    base_url = site_config["url"]
    list_path = site_config.get("list_path", "/tzgg/list.htm")
    site_name = site_config["name"]
    full_url = urljoin(base_url, list_path)

    print(f"  [{site_name}] Fetching {full_url}...")

    html = fetch_page(full_url)
    if not html:
        print(f"  [{site_name}] Failed to fetch")
        return []

    if len(html) < 500 or "window.location" in html:
        print(f"  [{site_name}] Got anti-bot page, trying alternative...")
        alt_paths = ["/index.htm", "/tzgg.htm", "/news.htm", "/"]
        for alt in alt_paths:
            alt_url = urljoin(base_url, alt)
            html = fetch_page(alt_url)
            if html and len(html) > 500 and "window.location" not in html:
                break

    notices = parse_notices(html, base_url, site_name)
    print(f"  [{site_name}] Found {len(notices)} notices")
    return notices

def scrape_all(config):
    all_notices = []
    for site in config.get("websites", []):
        notices = scrape_website(site)
        all_notices.extend(notices)
        time.sleep(random.uniform(2, 5))
    return all_notices
