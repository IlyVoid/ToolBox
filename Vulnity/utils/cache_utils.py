import os
import json
from datetime import datetime

def save_cache(url, results):
    os.makedirs("cache", exist_ok=True)
    filename = f"cache/{url.replace('http://', '').replace('https://', '').replace('/', '_')}_cache.json"
    with open(filename, "w") as file:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, file)

def load_cache(url):
    filename = f"cache/{url.replace('http://', '').replace('https://', '').replace('/', '_')}_cache.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return None
