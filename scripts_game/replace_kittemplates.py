#
# Script to replace kits' aitemplates
# Coder: [R-DEV]papadanku
#

# Import shared modules
from shared import Repo

class ReplaceKitTemplates(object):

    def __init__(self):
        self.object_path = ""
        self.file_paths = set()
        self.target_string = input("Insert kit files to target (e.g. spotter): ")
        self.template_target = input("Insert target kitTemplate (e.g. Assault): ")
        self.template_replace = input("Insert replacement kitTemplate (e.g. Spotter): ")

    def __call__(self):
        self.object_path = Repo.get_dir("objects", "kits")
        self.file_paths = Repo.get_files(self.object_path, ".tweak")
        self.replace_templates()

    def replace_templates(self):
        TARGET = f"ObjectTemplate.aiTemplate {self.template_target}"
        REPLACE = f"ObjectTemplate.aiTemplate {self.template_replace}"

        for path in self.file_paths:
            if (self.target_string in path):
                file_str = ""
                with open(path, "r") as file:
                    file_str = file.read().replace(TARGET, REPLACE)
                with open(path, "w") as file:
                    file.write(file_str)


app = ReplaceKitTemplates()
app()
