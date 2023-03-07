#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os

# File information

file_extensions = {
    ".ai",
    ".tweak"
}

file_paths = {
    ".ai": set(),
    ".tweak": set()
}

template_words = {
    "aiTemplate.create",
    "aiTemplatePlugin.create",
    "kitTemplate.create",
    "weaponTemplate.create"
}

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
        for line in file:
            template_str = line.strip().split(" ")
            if template_str[0] in template_words:
                aitemplates.add(template_str[1])

# [3] See if aiTemplate in file exists
for path in file_paths[".tweak"]:
    with open(path, "r") as file:
        for line in file:
            if (".aiTemplate" in line) and ("rem" in line):
                template = line.strip().split(" ")[-1]
                if template not in aitemplates:
                    string = f"{path}\n{template}"
                    print(string)
