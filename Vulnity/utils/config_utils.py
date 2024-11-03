import json
import os

def load_endpoints():
    config_path = os.path.join("config", "endpoints.json")
    with open(config_path, "r") as file:
        data = json.load(file)
    return data.get("endpoints", [])
