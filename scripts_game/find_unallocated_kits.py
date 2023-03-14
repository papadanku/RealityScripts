#
# Script to detect missing allocated kits in a repository
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

# Data
faction_paths = []

# [1] Get all kit files
for root, dir, files, in os.walk(object_path):
    for file_name in files:
        if "variants.inc" in file_name:
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            faction_paths.append(file_path)

# Methods to get a types of kits
class Kits(object):
    @staticmethod
    def loaded(file_path):
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("ObjectTemplate.create"):
                    return line.strip().split()[-1]

    @staticmethod
    def allocated(file_path):
        kits_allocated = set()
        with open(file_path) as file:
            for line in file:
                if line.startswith("ObjectTemplate.setObjectTemplate"):
                    kit = line.strip().split()[-1]
                    kits_allocated.add(kit)
        return kits_allocated

    @staticmethod
    def unallocated(file_path):
        faction = file_path.split("\\")[-2]
        faction_kits = {}
        variant = ""

        # Get missing files
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip().split()
                if "endIf" in line:
                    break
                # Get variant invokation
                if "v_arg1" in line:
                    variant = line[-1].replace('"', "")
                    faction_kits[variant] = dict(loaded=set(), allocated=set())
                    continue
                elif "else" in line:
                    variant = f"{faction}_default"
                    faction_kits[variant] = dict(loaded=set(), allocated=set())
                    continue
                # Only add if a variant's loaded
                if variant and faction:
                    path = os.path.join(object_path, faction, line[-1])
                    if "preload" in os.path.abspath(path):
                        faction_kits[variant]["allocated"] = Kits.allocated(path)
                    elif "preload" not in path:
                        faction_kits[variant]["loaded"].add(Kits.loaded(path))
                        continue

            # Print missing kits within faction
            for variant in faction_kits.keys():
                loaded = faction_kits[variant]["loaded"]
                allocated = faction_kits[variant]["allocated"]
                difference = loaded.difference(allocated)
                if difference:
                    print(f"[{variant}] has missing templates: {difference}")

# [2] Get all missing templates
for faction in faction_paths:
    Kits.unallocated(faction)
