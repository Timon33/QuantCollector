import os
import json
import logging

# load and read config
logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = "config.json"


def load_config():
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)

    except Exception as e:
        logger.critical(f"Can't load config. Aborting!\n{e}")
        exit(1)

    return config_json


def get_config():
    return CONFIG_DICT


def get_secret():
    try:
        with open(get_config()["secret"], "r") as f:
            secrets = f.read()
            if secrets.isascii():
                return secrets
            else:
                logger.critical("Secret should only include printable characters! Aborting!")
    except IOError as e:
        logger.critical(f"Api secret file not found! Aborting!\n{e}")
    exit(1)


CONFIG_DICT = load_config()
