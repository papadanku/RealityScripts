"""
Library to process .ai files
"""

# Import Python modules
import re

# Import shared modules
import shared


class FindShaderTechniques(shared.Application):

    def __init__(self, repo_path):
        super().__init__(repo_path, "shaders")
        self.file_paths = {}
        self.extensions = {".fx"}
        for extension in self.extensions:
            self.file_paths[extension] = set()
        self.techniques = {}

    def __call__(self):
        super().get_files(self.extensions)
        self.get_techniques()
        for shader, techniques in self.techniques.items():
            if techniques:
                print("%s \n %s" % (shader, str(techniques)))

    def get_techniques(self):
        # Fetch all techniques from the directory
        pattern = re.compile(r"technique (\w+)", re.MULTILINE)
        for path in self.file_paths[".fx"]:
            with open(path, "r") as file:
                techniques = re.findall(pattern, file.read())
                self.techniques.update({path: techniques})
