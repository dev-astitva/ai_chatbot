import json
import os

CONFIG_FILE = "user_config.json"
DEFAULT_CONF = {
    "google_api_key": "",
    "news_api_key": "",
    "weather_api_key": "",
    "news_prefs": "technology,AI,business"
}

def load_conf():
    if not os.path.exists(CONFIG_FILE):
        save_conf(DEFAULT_CONF)
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_conf(conf):
    with open(CONFIG_FILE, "w") as file:
        json.dump(conf, file, indent=2)
