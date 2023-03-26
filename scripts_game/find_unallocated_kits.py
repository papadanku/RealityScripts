#
# Script to detect missing allocated kits in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# Get repository path
def get_folder_path(*args):
    repo_path = input("Input repository path: ")
    target_path = os.path.join(repo_path, "\\".join(args))
    return os.path.abspath(target_path)

object_path = get_folder_path("objects", "kits")

# App information
data = {
    "factions": [],
    "patterns": {
        "loaded": re.compile("(?<=ObjectTemplate\\.create\\sKit\\s)\\w+"),
        "allocated": re.compile("(?<=ObjectTemplate.setObjectTemplate...)\\w+")
    }
}

# [1] Get all kit files
for root, dir, files, in os.walk(object_path):
    for file_name in files:
        if "variants.inc" in file_name:
            dir_path = os.path.realpath(root)
            file_path = os.path.join(dir_path, file_name)
            data["factions"].append(file_path)

# Methods to get a types of kits
class Kits(object):
    @staticmethod
    def get_loaded(file_path):
        with open(file_path, "r") as file:
            kit = re.search(data["patterns"]["loaded"], file.read())
            if kit:
                return kit.group()

    @staticmethod
    def get_allocated(file_path):
        with open(file_path) as file:
            return set(re.findall(data["patterns"]["allocated"], file.read()))

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
                        faction_kits[variant]["allocated"] = Kits.get_allocated(path)
                    elif "preload" not in path:
                        faction_kits[variant]["loaded"].add(Kits.get_loaded(path))
                        continue

            # Print missing kits within faction
            for variant in faction_kits.keys():
                loaded = faction_kits[variant]["loaded"]
                allocated = faction_kits[variant]["allocated"]
                difference = loaded.difference(allocated)
                if difference:
                    print(f"[{variant}] has missing templates: {difference}")

# [2] Get all missing templates
for faction in data["factions"]:
    Kits.unallocated(faction)
