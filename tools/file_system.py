import os
import shutil
import json
import datetime


def rec_walk(path, depth=-1):
    if os.path.isdir(path) and depth != 0:
        return {name: rec_walk(os.path.join(path, name), depth - 1) for name in os.listdir(path)}
    else:
        return dict()


def folder_structure_to_json():
    root = json.load(open("config.json", "r"))["save_location"]
    structure = rec_walk(root, 3)
    with open("formats.json", "r") as f:
        formats = json.load(f)
        formats["structure"] = structure
    with open("formats.json", "w") as f:
        json.dump(formats, f, indent=4)


folder_structure_to_json()

