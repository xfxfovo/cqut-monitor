import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

def generate_id(title, url):
    content = f"{title}:{url}"
    return hashlib.md5(content.encode("utf-8")).hexdigest()

async def scrape_with_browser(url, timeout=30000):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent=random.choice(USER_AGENTS),
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            await page.wait_for_timeout(3000)
            content = await page.content()
            await browser.close()
            return content
        except Exception as e:
            print(f"  Browser error: {e}")
            await browser.close()
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
    ]

    items = []
    for sel in selectors:
        items = soup.select(sel)
        if items:
            break

    if not items:
        items = soup.select("li a[href]")

    for item in items[:30]:
        try:
            if item.name == "a":
                link_tag = item
            else:
                link_tag = item.select_one("a[href]")

            if not link_tag or not link_tag.get("href"):
                continue

            href = link_tag["href"]
            if href.startswith("javascript") or href == "#":
                continue

            full_link = urljoin(base_url, href)
            title = link_tag.get_text(strip=True)

            if not title or len(title) < 4:
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

async def scrape_website(site_config):
    base_url = site_config["url"]
    list_path = site_config.get("list_path", "/tzgg/list.htm")
    site_name = site_config["name"]
    full_url = urljoin(base_url, list_path)

    print(f"  [{site_name}] Scraping {full_url}...")

    html = await scrape_with_browser(full_url)
    if not html:
        return []

    notices = parse_notices(html, base_url, site_name)
    print(f"  [{site_name}] Found {len(notices)} notices")
    return notices

async def scrape_all(config):
    all_notices = []
    for site in config.get("websites", []):
        notices = await scrape_website(site)
        all_notices.extend(notices)
        await asyncio.sleep(random.uniform(2, 5))
    return all_notices
