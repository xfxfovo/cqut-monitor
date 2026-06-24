import os
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"
import time
import hashlib
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def generate_id(title, url):
    return hashlib.md5(f"{title}:{url}".encode("utf-8")).hexdigest()

def scrape_all(config):
    all_notices = []
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        for site in config.get("websites", []):
            base_url = site["url"]
            list_path = site.get("list_path", "/index.htm")
            site_name = site["name"]
            full_url = urljoin(base_url, list_path)
            print(f"  [{site_name}] {full_url}")

            page = browser.new_page()
            try:
                page.goto(full_url, wait_until="networkidle", timeout=45000)
                page.wait_for_timeout(10000)

                actual_url = page.url
                html = page.content()
                soup = BeautifulSoup(html, "lxml")

                notices = []
                for a in soup.find_all("a"):
                    href = a.get("href", "")
                    if "info/" not in href and "list" not in href:
                        continue
                    text = a.get_text(strip=True)
                    if not text or len(text) < 5:
                        continue
                    full_link = urljoin(actual_url, href)
                    notice_id = generate_id(text, full_link)
                    notices.append({
                        "id": notice_id,
                        "title": text,
                        "url": full_link,
                        "date": "",
                        "source": site_name,
                    })

                print(f"  [{site_name}] {len(notices)} notices")
                all_notices.extend(notices)

            except Exception as e:
                print(f"  [{site_name}] Error: {e}")
            finally:
                page.close()

            time.sleep(3)

        browser.close()

    return all_notices
