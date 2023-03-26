#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# App information
data = {
    "extensions": {
        ".ai",
        ".tweak"
    },

    "paths": {
        ".ai": set(),
        ".tweak": set()
    },

    "patterns": {
        "keywords": re.compile("[ai|kit|weapon]+Template\\.create\\s\\w+"),
        "template": re.compile("(?<=\\.aiTemplate\\s)\\w+")
    },

    "templates": set()
}

# Get repository path
def get_folder_path(*args):
    repo_path = input("Input repository path: ")
    target_path = os.path.join(repo_path, "\\".join(args))
    return os.path.abspath(target_path)

object_path = get_folder_path("objects")

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
        for word in re.findall(data["patterns"]["keywords"], file.read()):
            data["templates"].add(word.split()[-1])

# [3] See if aiTemplate in file exists
for object_file in data["paths"][".tweak"]:
    with open(object_file, "r") as file:
        template = re.search(data["patterns"]["template"], file.read())
        if template:
            template_str = template.group()
            if template_str not in data["templates"]:
                print("\n".join(["", object_file, template_str]))
