#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import fileinput
import os
import re

# File information

file_extensions = {
    ".ai",
    ".tweak"
}

file_paths = {
    ".ai": set(),
    ".tweak": set()
}

template_words = "|".join([
    "aiTemplate.create \\w+",
    "aiTemplatePlugin.create \\w+",
    "kitTemplate.create \\w+",
    "weaponTemplate.create \\w+"
    ])

aitemplates = set()

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
        if file_extension in file_extensions:
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            file_paths[file_extension].add(file_path)

# [2] Get created aitemplates
for path in file_paths[".ai"]:
    with open(path, "r") as file:
        file_content = file.read()
        for word in re.findall(f"({template_words})", file_content):
            aitemplates.add(word.split()[-1])

# [3] See if aiTemplate in file exists
with fileinput.FileInput(file_paths[".tweak"]) as input:
    for line in input:
        if (".aiTemplate" in line) and ("rem" not in line):
            template = line.strip().split(" ")[-1]
            if template not in aitemplates:
                string = f"{input.filename()}\n{template}"
                print(string)
