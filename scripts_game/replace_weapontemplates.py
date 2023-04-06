#
# Script to replace weapons' aitemplates with variants
# Coder: [R-DEV]papadanku
#

# Import Python modules
import re
import os

# Get repository path
def get_folder_path(*args):
    repo_path = input("Input repository path: ")
    target_path = os.path.join(repo_path, "\\".join(args))
    return os.path.abspath(target_path)

object_path = get_folder_path("objects", "weapons", "Handheld")

# App data
data = {
    "file_paths": set(),
    "pattern": re.compile(r'include ../../common/recoil.con "assaultrifle" ".*?" ".*?" "(.*?)"'),
    "aitemplate_str": "ObjectTemplate.aiTemplate"
}

# [1] Get all weapon configuration files
for root, dir, files, in os.walk(object_path):
    for file_name in files:
        if file_name.endswith(".tweak"):
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            data["file_paths"].add(file_path)

# [2] Process specific weapon files
for path in data["file_paths"]:
    with open(path, "r") as input_file:
        file_text = input_file.read()

        # Only process if the file has our specified pattern
        # NOTE: Hardcoded pattern is assault rifle
        if data["aitemplate_str"] in file_text:
            template = re.findall(data["pattern"], file_text)
            if template:
                weapon_variant = str(template[-1])
                old_variant = f'{data["aitemplate_str"]} ar_ai'
                new_variant = f'{data["aitemplate_str"]} ar_{weapon_variant}_ai'
                with open(path, "w") as output_file:
                    new_text = file_text.replace(old_variant, new_variant)
                    output_file.write(new_text)
