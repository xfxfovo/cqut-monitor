import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import load_config, get_pushplus_token, get_notified_ids, save_notified_ids
from src.scraper import scrape_all
from src.analyzer import analyze_notices
from src.notifier import send_notification

def main():
    print("=" * 50)
    print("CQUT Notification Monitor")
    print("=" * 50)

    config = load_config()
    token = get_pushplus_token()

    if not token:
        print("[ERROR] PUSHPLUS_TOKEN not set in config.json!")
        return

    notified_ids = get_notified_ids()

    print(f"[*] Previously notified: {len(notified_ids)} notices")
    print("[*] Scraping websites...")
    all_notices = scrape_all(config)
    print(f"[*] Found {len(all_notices)} notices total")

    if not all_notices:
        print("[*] No notices found (offline?). Will retry next time.")
        return

    new_notices = [n for n in all_notices if n["id"] not in notified_ids]
    print(f"[*] {len(new_notices)} new notices since last check")

    if not new_notices:
        print("[*] No new notices. Done.")
        return

    print("[*] Analyzing relevance...")
    relevant_notices = analyze_notices(new_notices, config)
    print(f"[*] {len(relevant_notices)} relevant notices")

    if relevant_notices:
        print("[*] Sending notification...")
        send_notification(token, relevant_notices, config)

    new_ids = notified_ids | {n["id"] for n in all_notices}
    save_notified_ids(new_ids)
    print(f"[*] Saved {len(new_ids)} notified IDs")
    print("[*] Done!")

if __name__ == "__main__":
    main()
