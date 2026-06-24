import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cache")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_pushplus_token():
    token = os.environ.get("PUSHPLUS_TOKEN", "")
    if token:
        return token
    config = load_config()
    return config.get("pushplus_token", "")

def get_notified_ids():
    cache_file = os.path.join(CACHE_DIR, "notified_ids.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_notified_ids(ids):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, "notified_ids.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(list(ids), f)
