
"""
Scripts to process files in Project Reality: BF2
Author: [R-DEV]papadanku
"""

# Import shared modules
from realityscripts import ai
from realityscripts import kits
from realityscripts import weapons

def main():
    try:
        path = input("Insert repo path: ")
    except:
        print("Not a valid path")
    
    app = ai.FindAITemplates(path)
    app = kits.CheckKitTemplates(path)
    app = weapons.ReplaceWeaponTemplates(path)


if __name__ == "__main__":
    main()
