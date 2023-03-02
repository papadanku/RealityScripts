#
# Script to replace kits' aitemplates
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os

objectPath = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\objects\kits"

# Arguments
kitTarget = "riflemanat"
kitTemplateSrc = "AT" 
kitTemplateDst = "LAT"

# Kit data
kitFilePaths = set()

# [1] Get all kit files
for root, dir, files, in os.walk(objectPath):
    for fileName in files:
        if (".tweak" in fileName) and (kitTarget in fileName):
            realDirPath = os.path.realpath(root)
            realFilePath = os.path.join(realDirPath, fileName)
            kitFilePaths.add(realFilePath)

# [2] Overwrite files
for kitPath in kitFilePaths:
    fileText = str()
    with open(kitPath, "r") as file:
        src = " ".join(["ObjectTemplate.aiTemplate", kitTemplateSrc])
        dst = " ".join(["ObjectTemplate.aiTemplate", kitTemplateDst])
        fileText = file.read().replace(src, dst)
    with open(kitPath, "w") as file:
        file.write(fileText)
