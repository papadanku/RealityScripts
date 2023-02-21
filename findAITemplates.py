#
# Script to detect missing aiTemplates in a repository
# Coder: [R-DEV]papadanku
#

import os

# Directory information
objectPath = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\objects"

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
def getFilePaths(path, extension) -> list:
    """
    Gets all of the files in the directory that ends with an extension
    """
    fileList = list()
    for root, dir, files, in os.walk(path):
        for fileName in files:
            if extension in fileName:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                fileList.append(realFilePath)
    return fileList

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

# [1] Get all AI and object files
for fileType in filePathDict.keys():
    filePathDict[fileType] = getFilePaths(objectPath, fileType)

# [2] Get created aiTemplates
for path in filePathDict[".ai"]:
    with open(path, "r") as file:
        for line in file:
            addTemplates(line.strip())

# [3] See if aiTemplate in file exists
for filePath in filePathDict[".tweak"]:
    findTemplates(filePath)
