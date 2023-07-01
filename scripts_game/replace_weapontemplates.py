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
        PATTERN_WEAPON = "assaultrifle"
        PATTERN_TEMPLATE = "ObjectTemplate.aiTemplate"
        PATTERN_VARIANT = re.compile('(?<=recoil\.con).*?("\w+")\n')

        for path in self.file_paths:
            with open(path, "r") as file:
                file_text = file.read()
                weapon = re.search(PATTERN_WEAPON, file_text)
                template = re.search(PATTERN_TEMPLATE, file_text)
                variant = re.search(PATTERN_VARIANT, file_text)
                if weapon and template and variant:
                    weapon_variant = variant.group()
                    old_variant = f'{PATTERN_TEMPLATE} ar_ai'
                    new_variant = f'{PATTERN_TEMPLATE} ar_{weapon_variant}_ai'
                    with open(path, "w") as output_file:
                        new_text = file_text.replace(old_variant, new_variant)
                        output_file.write(new_text)


app = ReplaceWeaponTemplates()
app()
