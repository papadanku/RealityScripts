#
# Script to detect missing aiTemplates in a repository
# Coder: [R-DEV]papadanku
#

import os

# File information

extensions = { ".ai", ".tweak" }

filePathDict = {
    ".ai": set(),
    ".tweak": set()
}

templateKeyWords = {
    "aiTemplate.create",
    "aiTemplatePlugin.create",
    "kitTemplate.create",
    "weaponTemplate.create"
}

aiTemplates = set()

# Main operations

objectPath = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\objects"

# [1] Get all AI and object files

for root, dir, files, in os.walk(objectPath):
    for fileName in files:
        fileExtension = os.path.splitext(fileName)[-1]
        if fileExtension in extensions:
            realDirPath = os.path.realpath(root)
            realFilePath = os.path.join(realDirPath, fileName)
            filePathDict[fileExtension].add(realFilePath)

# [2] Get created aiTemplates

def addTemplates(line):
    templateString = line.split(" ")
    if templateString[0] in templateKeyWords:
        aiTemplates.add(templateString[1])

for path in filePathDict[".ai"]:
    with open(path, "r") as file:
        for line in file:
            addTemplates(line.strip())

# [3] See if aiTemplate in file exists

for filePath in filePathDict[".tweak"]:
    with open(filePath, "r") as file:
        for line in file:
            if (".aiTemplate" not in line) or ("rem" in line):
                continue
            aiTemplate = line.strip().split(" ")[-1]
            if aiTemplate not in aiTemplates:
                string = f"{filePath}\n{aiTemplate}"
                print(string)
