"""
Library to process .ai files
"""

# Import Python modules
import re

# Import shared modules
from realityscripts import shared


class FindAITemplates(shared.Application):

    def __init__(self, repo_path):
        super().__init__(repo_path, "objects")
        self.extensions = {".ai", ".tweak"}
        for extension in self.extensions:
            self.file_paths[extension] = set()
        self.ai = set()

    def __call__(self):
        super().get_files(self.extensions)
        self.get_ai_templates()
        self.check_ai_templates()

    def get_ai_templates(self):
        # Fetch all created aiTemplates from the repo
        pattern = re.compile(r'(?:ai|kit|weapon)Template(?:Plugin)?\.create (\w+)')
        for path in self.file_paths[".ai"]:
            with open(path, "r") as file:
                self.ai.update(re.findall(pattern, file.read()))

    def check_ai_templates(self):
        # Check if the aiTemplate exists in the repo
        pattern = re.compile(r'(?<=\.aiTemplate )(\w+)')
        for object_file in self.file_paths[".tweak"]:
            with open(object_file, "r") as file:
                try:
                    template = re.search(pattern, file.read()).group()
                    if template not in self.ai:
                        print("\n".join(["", object_file, template]))
                except:
                    continue
