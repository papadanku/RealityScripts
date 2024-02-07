import os
from typing import Any


class Application(object):

    def __init__(self, repo_path, dir):
        self.path = os.path.abspath(os.path.join(repo_path, dir))
        self.file_paths = {}

    def __call__(self):
        pass

    def get_files(self, extensions):
        for root, _, files in os.walk(self.path):
            for file in files:
                extension = os.path.splitext(file)[-1]
                if extension in extensions:
                    dir_path = os.path.realpath(root)
                    file_path = os.path.join(dir_path, file)
                    self.file_paths[extension].add(file_path)
