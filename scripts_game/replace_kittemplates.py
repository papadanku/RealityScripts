#
# Script to replace kits' aitemplates
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os

# Get repository path
def get_folder_path(*args):
    repo_path = input("Input repository path: ")
    target_path = os.path.join(repo_path, "\\".join(args))
    return os.path.abspath(target_path)

object_path = get_folder_path("objects", "kits")

# Arguments
target_str = "spotter"
template_target = "Assault" 
template_replace = "Spotter"

# Kit data
file_paths = set()

# [1] Get all kit files
for root, dir, files, in os.walk(object_path):
    for file_name in files:
        if file_name.endswith(".tweak") and (target_str in file_name):
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            file_paths.add(file_path)

# [2] Overwrite files
for path in file_paths:
    file_str = str()
    with open(path, "r") as file:
        src = " ".join(["ObjectTemplate.aiTemplate", template_target])
        dst = " ".join(["ObjectTemplate.aiTemplate", template_replace])
        file_str = file.read().replace(src, dst)
    with open(path, "w") as file:
        file.write(file_str)
