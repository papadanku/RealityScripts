#
# Script to detect missing pre-allocated kits in a repository
# Coder: [R-DEV]papadanku
#

# Import Python modules
import os
import re

# Import shared modules
from shared import Repo

class Patterns(object):
    KIT_VARIANTS = re.compile('("\w+"|else\b)(.*?)(?=else|$)', re.DOTALL)
    KIT_FILE_PATHS = re.compile('run (.*?\.tweak)')
    ALLOCATED_KIT_NAMES = re.compile('(?:ObjectTemplate\.setObjectTemplate \d) (\w+)')
    LOADED_KIT_NAME = re.compile('(?:ObjectTemplate.create Kit) (\w+)')

class CheckKitTemplates(object):

    def __init__(self):
        self.object_path = ""
        self.file_paths = set()
    
    def __call__(self):
        """
        Fetches kit variant files in the give repository
        """
        self.object_path = Repo.get_dir("objects", "kits")
        self.file_paths = Repo.get_files(self.object_path, "variants.inc")
        for variants_path in self.file_paths:
            self.search_variants(variants_path)

    def check_kits(self, faction, variant, kits):
        kit_file_paths = re.findall(Patterns.KIT_FILE_PATHS, kits)
        kits = { 'load': set(), 'alloc': set() }

        # Allocate kits from the variant runs and preloaded
        for path in kit_file_paths:
            file_path = os.path.join(self.object_path, faction, path)
            with open(file_path, "r") as file:
                if "preload" in path:
                    kits['alloc'].update(re.findall(Patterns.ALLOCATED_KIT_NAMES, file.read()))
                else:
                    kits['load'].update(re.findall(Patterns.LOADED_KIT_NAME, file.read()))

        # Calculate the differences between the two
        missing_kits = kits['load'] - kits['alloc']
        if len(missing_kits) == 0:
            print(f'{variant}: no missing kits')
        else:
            print(f'{variant}: {missing_kits}')

    def search_variants(self, path):
        """
        1. Fetches for individual variants within the given variant file
        2. Checks each variant for missing pre-allocated kits
        """
        faction = path.split('\\')[-2]
        with open(path, "r") as file:
            variants = re.findall(Patterns.KIT_VARIANTS, file.read())
            for variant, kits in variants:
                self.check_kits(faction, variant, kits)

app = CheckKitTemplates()
app()
