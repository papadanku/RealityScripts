#
# Script to detect missing aiTemplates in a repository
# Coder: [R-DEV]papadanku
#

import os

# File information

filePathDict = {
    ".ai": list(),
    ".tweak": list()
}

aiDict = {
    "keywords": (
        "aitemplate.create",
        "aitemplateplugin.create",
        "kittemplate.create",
        "weapontemplate.create"
    ),
    "templates": list()
}

# Main operations

objectPath = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\objects"

# [1] Get all AI and object files

for root, dir, files, in os.walk(objectPath):
    for fileName in files:
        for extension in filePathDict.keys():
            if extension in fileName:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathDict[extension].append(realFilePath)

# [2] Get created aiTemplates

def addTemplates(line):
    for keyWord in aiDict["keywords"]:
        if keyWord in line.lower():
            aiTemplate = line.split(" ")[1]
            aiDict["templates"].append(aiTemplate)

for path in filePathDict[".ai"]:
    with open(path, "r") as file:
        for line in file:
            addTemplates(line.strip())

# [3] See if aiTemplate in file exists

def isValidTemplate(line):
    for aiTemplate in aiDict["templates"]:
        if aiTemplate in line:
            return True
    return False

for filePath in filePathDict[".tweak"]:
    with open(filePath, "r") as file:
        for line in file:
            if (".aiTemplate" not in line) or ("rem" in line):
                continue
            if isValidTemplate(line) is False:
                aiTemplate = line.split(" ")[-1]
                string = f"{filePath}\n{aiTemplate}"
                print(string)
