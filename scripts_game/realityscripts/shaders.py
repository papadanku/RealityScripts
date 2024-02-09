"""
Library to process .ai files
"""

# Import Python modules
import glob
import math
import re

# Import shared modules
from realityscripts import shared


class FindShaderTechniques(shared.Application):

    def __init__(self, repo_path):
        super().__init__(repo_path, "shaders")
        self.file_paths = []
        self.techniques = {}

    def __call__(self):
        self.get_techniques()
        for shader, techniques in self.techniques.items():
            if techniques:
                print("%s \n %s" % (shader, str(techniques)))

    def get_techniques(self):
        """
        Fetch all techniques from the directory
        """

        PATTERN = re.compile(r"technique (\w+)", re.MULTILINE)
        self.file_paths = glob.glob("/".join([self.path, "*.fx*"]), recursive=True)
        for path in self.file_paths:
            with open(path, "r") as file:
                techniques = re.findall(PATTERN, file.read())
                self.techniques.update({path: techniques})


class LinearizeMapData(shared.Application):

    def __init__(self, repo_path):
        super().__init__(repo_path, "levels")
        self.file_paths = set()
        self.get_files()

    def linearize(self, path):
        with open(path, "r") as file:
            file_text = file.read()

            # Gamma-correct fog settings
            color_settings = re.findall(r"(?i)(\S+color) (.*)", file_text, re.MULTILINE)
            for setting, value in color_settings:
                rgb = map(float, value.split("/"))

                if ("Fog" in setting) or ("fog" in setting):
                    rgb = list(map(lambda x: math.pow(x / 255.0, 2.2) * 255.0, rgb))
                else:
                    rgb = list(map(lambda x: math.pow(x / 255.0, 2.2), rgb))

                new_color_settings = setting + " " + "/".join(map(str, rgb))
                file_text = file_text.replace(" ".join([setting, value]), new_color_settings)

            with open(path, "w") as file:
                file.write(file_text)

    def get_files(self):
        self.file_paths.update(glob.glob("\\".join([self.path, "*", "sky*.con"])))
        self.file_paths.update(glob.glob("\\".join([self.path, "*", "water*.con"])))

        for path in self.file_paths:
            self.linearize(path)
