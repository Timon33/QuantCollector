import os
import json

CONFIG_FILE_NAME = "config.json"

def root_dir():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def load_config():
    config_path = os.path.join(root_dir(), CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)
    
    except Exception as e:
        print(f"can't load config.\n{e}")
        exit()

    return config_json

def save_location() -> str:
    return load_config()["save_location"]

def api_type() -> str:
    return load_config()["api_type"]

def symbol_list() -> list:
    file_name = load_config()["symbol_list_file"]
    with open(os.path.join(root_dir(), file_name), "r") as f:
        return json.load(f)
