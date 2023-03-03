#
# Script to detect missing allocated kits in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os

# Get repository path
def getFolderLocation(*args):
    repoPath = input("Input repository path: ")
    targetPath = os.path.join(repoPath, "\\".join(args))
    return os.path.abspath(targetPath)

objectPath = getFolderLocation("objects", "kits")

# Data
factionFilePaths = list()

# [1] Get all kit files
for root, dir, files, in os.walk(objectPath):
    for fileName in files:
        if "variants.inc" in fileName:
            realDirPath = os.path.realpath(root)
            realFilePath = os.path.join(realDirPath, fileName)
            factionFilePaths.append(realFilePath)

# Methods to get a types of kits
class getKits(object):
    @staticmethod
    def loaded(filePath):
        with open(filePath, "r") as file:
            for line in file:
                if "ObjectTemplate.create" in line:
                    return line.strip().split(" ")[-1]

    @staticmethod
    def allocated(filePath):
        allocatedKits = set()
        with open(filePath) as file:
            for line in file:
<<<<<<< Updated upstream
                kit = line.strip().split(" ")[-1]
                if "ObjectTemplate.setObjectTemplate" in line:
=======
                if "ObjectTemplate.setObjectTemplate" in line:
                    kit = line.strip().split(" ")[-1]
>>>>>>> Stashed changes
                    allocatedKits.add(kit)
        return allocatedKits

    @staticmethod
    def unallocated(filePath):
        faction = filePath.split("\\")[-2]
        factionKits = dict()
        variant = str()

        # Get missing files
        with open(filePath, "r") as file:
            for line in file:
                if "endIf" in line:
                    break
                # Get variant invokation
                if "v_arg1" in line:
                    variant = line.strip().split(" ")[-1].replace('"', "")
                    factionKits[variant] = dict(loaded=set(), allocated=set())
                    continue
                elif "else" in line:
                    variant = f"{faction}_default"
                    factionKits[variant] = dict(loaded=set(), allocated=set())
                    continue
                # Only add if a variant's loaded
                if variant and faction:
                    line = line.strip().split(" ")[-1]
                    path = os.path.join(objectPath, faction, line)
                    path = path.replace("\\", "/")
                    if "preload" in path:
                        factionKits[variant]["allocated"] = getKits.allocated(path)
                    elif "preload" not in line:
                        factionKits[variant]["loaded"].add(getKits.loaded(path))
                        continue

            # Print missing kits within faction
            for variant in factionKits.keys():
                loaded = factionKits[variant]["loaded"]
                allocated = factionKits[variant]["allocated"]
                difference = loaded.difference(allocated)
                if difference:
                    print(f"[{variant}] has missing templates: {difference}")

# [2] Get all missing templates
for faction in factionFilePaths:
    getKits.unallocated(faction)
