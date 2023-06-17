#
# Script to replace weapons' aitemplates with variants
# Coder: [R-DEV]papadanku
#

# Import Python modules
import re

# Import shared modules
from shared import repo

# App data
data = {
    "file_paths": set(),
    "pattern": re.compile(r'include ../../common/recoil.con "assaultrifle" ".*?" ".*?" "(.*?)"'),
    "aitemplate_str": "ObjectTemplate.aiTemplate"
}

# Get repository path
object_path = repo.get_dir("objects", "weapons", "Handheld")

# [1] Get all weapon configuration files
data["file_paths"] = repo.get_files(object_path, {".tweak"})

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
