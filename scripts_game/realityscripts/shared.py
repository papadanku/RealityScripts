
import os

class Application(object):

    def __init__(self, path: str, *args):
        self.path = os.path.abspath(os.path.join(path, "\\".join(args)))
        self.extensions = set()
        self.file_paths = { }

    def get_files(self):
        for root, _, files, in os.walk(self.path):
            for file in files:
                extension = os.path.splitext(file)[-1]
                if extension in self.extensions:
                    dir_path = os.path.realpath(root)
                    file_path = os.path.join(dir_path, file)
                    self.file_paths[extension].add(file_path)
