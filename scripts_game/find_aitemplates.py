#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# Import shared modules
from shared import repo

# App information
data = {
    "aitemplates": set(),
    "extensions": { ".ai", ".tweak" },
    "paths": {
        ".ai": set(),
        ".tweak": set()
    },
    "patterns": {
        "keywords": re.compile('(?:ai|kit|weapon)Template(?:Plugin)?\.create (\w+)'),
        "aitemplate": re.compile('(?<=\.aiTemplate )(\w+)')
    },
}

# Get repository path
object_path = repo.get_dir("objects")

# [1] Get all AI and object files
for root, dir, files, in os.walk(object_path):
    for file_name in files:
        file_extension = os.path.splitext(file_name)[-1]
        if file_extension in data["extensions"]:
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            data["paths"][file_extension].add(file_path)

# [2] Get created aitemplates
for path in data["paths"][".ai"]:
    with open(path, "r") as file:
        templates = re.findall(data["patterns"]["keywords"], file.read())
        data["aitemplates"].update(templates)

# [3] See if aiTemplate in file exists
for object_file in data["paths"][".tweak"]:
    with open(object_file, "r") as file:
        template = re.search(data["patterns"]["aitemplate"], file.read())
        if not template:
            continue
        else:
            template_str = template.group()
            if template_str not in data["aitemplates"]:
                print("\n".join(["", object_file, template_str]))
