#
# Script to detect missing aitemplates in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# Import shared modules
from shared import Repo

class FindAITemplates(object):

    def __init__(self):
        self.object_path = ""
        self.file_paths = { ".ai": set(), ".tweak": set() }
        self.ai_templates = set()

    def __call__(self):
        self.object_path = Repo.get_dir("objects")
        self.get_files()
        self.get_templates()
        self.check_templates()

    def get_files(self):
        EXTENSIONS = { ".ai", ".tweak" }
        for root, dir, files, in os.walk(self.object_path):
            for file_name in files:
                file_extension = os.path.splitext(file_name)[-1]
                if file_extension in EXTENSIONS:
                    dir_path = os.path.realpath(root)
                    file_path = os.path.join(dir_path, file_name)
                    self.file_paths[file_extension].add(file_path)

    def get_templates(self):
        PATTERN = re.compile('(?:ai|kit|weapon)Template(?:Plugin)?\.create (\w+)')
        for path in self.file_paths[".ai"]:
            with open(path, "r") as file:
                templates = re.findall(PATTERN, file.read())
                self.ai_templates.update(templates)

    def check_templates(self):
        PATTERN_REM = re.compile('rem ObjectTemplate\.aiTemplate')
        PATTERN_CATCH = re.compile('(?<=\.aiTemplate )(\w+)')
        for object_file in self.file_paths[".tweak"]:
            with open(object_file, "r") as file:
                text = file.read()
                rem_template = re.search(PATTERN_REM, text)
                template = re.search(PATTERN_CATCH, text)
                # Continue if we are not calling an enabled "ObjectTemplate.aiTemplate"
                if rem_template or (template is None):
                    continue
                template_string = template.group()
                if template_string not in self.ai_templates:
                    print("\n".join(["", object_file, template_string]))


app = FindAITemplates()
app()
