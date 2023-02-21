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

# Gets all weapon file-paths from specified directory
def getFilePaths(path, extension) -> list:
    fileList = list()
    for root, dir, files, in os.walk(path):
        for fileName in files:
            if extension in fileName:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                fileList.append(realFilePath)
    return fileList

# Get all configuration files
for fileType in filePathDict.keys():
    filePathDict[fileType] = getFilePaths(objectPath, fileType)

# Get all created aiTemplates
def addTemplates(line):
    for templateLine in aiTemplateDict.keys():
        if templateLine in line.lower():
            line = line.split(" ")[1]
            aiTemplateDict[templateLine].append(line)

for path in filePathDict[".ai"]:
    with open(path, "r") as file:
        for line in file:
            addTemplates(line.strip())

# See if aiTemplate in file is valid
outputDict = dict()

def isValidTemplate(line):
    for validTemplateList in aiTemplateDict.values():
        for validTemplate in validTemplateList:
            if validTemplate in line:
                return True
    return False

def findTemplates(filePath):
    with open(filePath, "r") as file:
        outputDict[filePath] = list()
        for line in file:
            if (".aiTemplate" not in line) or ("rem" in line):
                continue
            elif isValidTemplate(line) is False:
                line = line.strip()
                printString = " ".join(["Missing aiTemplate:", line])
                print(printString)

for filePath in filePathDict[".tweak"]:
    findTemplates(filePath)
