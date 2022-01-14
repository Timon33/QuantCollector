import os
import json
import logging

# load and read config

CONFIG_FILE_NAME = "config.json"


def load_config():
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)

    except Exception as e:
        logger = logging.getLogger("main.config")
        logger.error(f"can't load config.\n{e}")
        exit()

    return config_json


def get_config():
    return CONFIG_DICT


CONFIG_DICT = load_config()
