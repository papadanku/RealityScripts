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

aiTemplateDict = {
    "aitemplate.create": list(),
    "aitemplateplugin.create": list(),
    "kittemplate.create": list(),
    "weapontemplate.create": list()
}

# Functions
def addTemplates(line):
    for templateLine in aiTemplateDict.keys():
        if templateLine in line.lower():
            line = line.split(" ")[1]
            aiTemplateDict[templateLine].append(line)

def isValidTemplate(line):
    for validTemplateList in aiTemplateDict.values():
        for validTemplate in validTemplateList:
            if validTemplate in line:
                return True
    return False

def findTemplates(filePath):
    with open(filePath, "r") as file:
        for line in file:
            if (".aiTemplate" not in line) or ("rem" in line):
                continue
            elif isValidTemplate(line) is False:
                line = line.strip()
                printString = " ".join(["Missing aiTemplate:", line])
                print(printString)

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
for path in filePathDict[".ai"]:
    with open(path, "r") as file:
        for line in file:
            addTemplates(line.strip())

# [3] See if aiTemplate in file exists
for filePath in filePathDict[".tweak"]:
    findTemplates(filePath)
