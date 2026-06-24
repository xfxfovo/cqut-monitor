import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
import time
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

def generate_id(title, url):
    content = f"{title}:{url}"
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def scrape_website(site_config):
    notices = []
    base_url = site_config["url"]
    list_path = site_config.get("list_path", "/tzgg/list.htm")
    site_name = site_config["name"]

    try:
        full_url = urljoin(base_url, list_path)
        resp = requests.get(full_url, headers=get_headers(), timeout=15, verify=False)
        resp.encoding = resp.apparent_encoding or "utf-8"

        if resp.status_code != 200:
            print(f"[{site_name}] HTTP {resp.status_code}: {full_url}")
            return notices

        soup = BeautifulSoup(resp.text, "lxml")

        list_items = soup.select("ul.news-list li, ul.list li, div.news-list li, table.list_table tr, div.list-item")
        if not list_items:
            list_items = soup.select("li a, td a, div.title a")

        for item in list_items[:30]:
            try:
                if item.name == "a":
                    link_tag = item
                else:
                    link_tag = item.select_one("a")

                if not link_tag or not link_tag.get("href"):
                    continue

                href = link_tag["href"]
                full_link = urljoin(base_url, href)

                title = link_tag.get_text(strip=True)
                if not title:
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
            except Exception as e:
                continue

        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"[{site_name}] Error: {e}")

    return notices

def scrape_all(config):
    all_notices = []
    for site in config.get("websites", []):
        notices = scrape_website(site)
        all_notices.extend(notices)
    return all_notices
