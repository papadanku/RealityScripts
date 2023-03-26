#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# App information
app = {
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
        if file_extension in app["extensions"]:
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            app["paths"][file_extension].add(file_path)

# [2] Get created aitemplates
for path in app["paths"][".ai"]:
    with open(path, "r") as file:
        file_content = file.read()
        for word in re.findall(app["patterns"]["keywords"], file_content):
            app["templates"].add(word.split()[-1])

# [3] See if aiTemplate in file exists
for object_file in app["paths"][".tweak"]:
    with open(object_file, "r") as file:
        file_content = file.read()
        template = re.search(app["patterns"]["template"], file_content)
        if template:
            template_str = template.group()
            if template_str not in app["templates"]:
                print("\n".join(["", object_file, template_str]))
