#
# Script to replace weapons' aitemplates with variants
# Coder: [R-DEV]papadanku
#

# Import Python modules
import re

# Import shared modules
from shared import Repo

class ReplaceWeaponTemplates(object):

    def __init__(self):
        self.object_path = ""
        self.file_paths = set()

    def __call__(self):
        self.object_path = Repo.get_dir("objects", "weapons", "Handheld")
        self.file_paths = Repo.get_files(self.object_path, ".tweak")
        self.replace_templates()

    def replace_templates(self):
        pattern_weapon = "assaultrifle"
        pattern_string = "ObjectTemplate.aiTemplate"
        pattern_variant = re.compile('(?<=recoil\.con).*?("\w+")\n')
        for path in self.file_paths:
            with open(path, "r") as file:
                file_text = file.read()
                weapon = re.search(pattern_weapon, file_text)
                template = re.search(pattern_string, file_text)
                variant = re.search(pattern_variant, file_text)
                if weapon and template and variant:
                    weapon_variant = variant.group()
                    old_variant = f'{pattern_string} ar_ai'
                    new_variant = f'{pattern_string} ar_{weapon_variant}_ai'
                    with open(path, "w") as output_file:
                        new_text = file_text.replace(old_variant, new_variant)
                        output_file.write(new_text)

app = ReplaceWeaponTemplates()
app()
