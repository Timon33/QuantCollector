import os
import json
import logging
import pystore

from typing import Union

# load and read config
logger = logging.getLogger(__name__)

# TODO find good way to set this
CONFIG_FILE_NAME = "config.json"
API_CONFIG_FOLDER = "api_config"

ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# (re)loads the config from disk
def load_config() -> dict:
    config_path = os.path.join(ABS_PATH, CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            return json.load(f)

    except Exception as e:
        logger.critical(f"Can't load config. Aborting!\n{e}")
        exit(1)


def get_config(*args) -> Union[str, dict]:
    try:
        # traverse config json dict using varargs
        conf = CONFIG_DICT
        for name in args:
            conf = conf[name]
        return conf

    except KeyError or TypeError as e:
        logger.critical(f"Entry for '{args}' not found!\n{e}\nAborting!")
        exit(1)


def get_api(name: str) -> dict:
    try:
        with open(os.path.join(ABS_PATH, API_CONFIG_FOLDER, f"{name}.json")) as f:
            return json.load(f)
    except IOError:
        logger.critical(f"can't find config for {name} api. Aborting!")
        exit(1)


def get_dataframe_types(typename: str):
    return get_config("dataframe_types", typename)


def get_loglevel() -> int:
    try:
        return getattr(logging, get_config("logging_level"))
    except AttributeError as e:
        logger.warning(
            f"Debug level specified in config not found. Defaulting to WARNING level.\n{e}")
        return logging.WARNING


def get_symbols() -> list:
    symbol_file_name = get_config("symbol_list_file")
    try:
        with open(os.path.join(ABS_PATH, symbol_file_name), "r") as f:
            return json.load(f).get("symbols", list())

    except IOError as e:
        logger.critical(
            f"Could not find symbols list file {symbol_file_name}\n{e}")
    except json.JSONDecodeError as e:
        logger.critical(f"Could not decode symbol list file\n{e}")

    exit(1)


def init_pystore():
    pystore.set_path(get_config("pystore", "path"))


def get_pystore():
    return pystore.store(get_config("pystore", "store"))


CONFIG_DICT = load_config()
init_pystore()
