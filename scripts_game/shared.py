
import os

class Repo(object):

    @staticmethod
    def get_dir(*args):
        repo_path = input("Input repository path: ")
        target_path = os.path.join(repo_path, "\\".join(args))
        return os.path.abspath(target_path)

    @staticmethod
    def get_files(path: str, included_string: str) -> set:
        paths = set()
        for root, dir, files, in os.walk(path):
            for file_name in files:
                if included_string in file_name:
                    paths.add(os.path.join(root, file_name))
        return paths
