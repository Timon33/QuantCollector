import os
import json
import logging

from typing import Union

# load and read config
logger = logging.getLogger(__name__)

# TODO find good way to set this
CONFIG_FILE_NAME = "config.json"

ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# (re)loads the config from disk
def load_config() -> dict:
    config_path = os.path.join(ABS_PATH, CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)

    except Exception as e:
        logger.critical(f"Can't load config. Aborting!\n{e}")
        exit(1)

    return config_json


def get_config(entry_name: str) -> Union[str, dict]:
    try:
        return CONFIG_DICT[entry_name]
    except KeyError as e:
        logger.critical(f"Entry for '{entry_name}' not found!\n{e}\nAborting!")
        exit(1)


def get_api(name) -> dict:
    try:
        return get_config("apis")[name]
    except KeyError:
        logger.error(f"Did not find configuration for api {name}!")
        return dict()


def get_secret(name: str):
    try:
        with open(os.path.join(ABS_PATH, get_api(name).get("secret")), "r") as f:
            return f.read()
    except IOError:
        logger.critical(f"Did not find secret for api {name}! Aborting!")
        exit(1)


def get_loglevel() -> int:
    try:
        return getattr(logging, get_config("logging_level"))
    except AttributeError as e:
        logger.warning(f"Debug level specified in config not found. Defaulting to WARNING level.\n{e}")
        return logging.WARNING


def get_symbols() -> list:
    try:
        with open(os.path.join(ABS_PATH, get_config("symbol_list_file")), "r") as f:
            return json.load(f).get("symbols", list())
    except IOError as e:
        logger.critical(f"Could not find symbols list file {get_config('symbol_list_file')}\n{e}")
        exit(1)
    except json.JSONDecodeError as e:
        logger.critical(f"Could not decode symbol list file\n{e}")
        exit(1)


CONFIG_DICT = load_config()
