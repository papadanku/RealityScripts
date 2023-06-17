#
# Script to replace kits' aitemplates
# Coder: [R-DEV]papadanku
#

# Import shared modules
from shared import repo

# Get repository path
object_path = repo.get_dir("objects", "kits")

# [1] Get all kit files
file_paths = repo.get_files(object_path, {".tweak"})

# Arguments
target_str = "spotter"
template_target = "Assault" 
template_replace = "Spotter"

# [2] Overwrite files
for path in file_paths:
    if (target_str in path):
        file_str = ""
        with open(path, "r") as file:
            src = f"ObjectTemplate.aiTemplate {template_target}"
            dest = f"ObjectTemplate.aiTemplate {template_replace}"
            file_str = file.read().replace(src, dest)
        with open(path, "w") as file:
            file.write(file_str)
