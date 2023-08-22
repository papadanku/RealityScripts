
"""
Library to process objects
"""

# Import Python modules
import os
import re

# Import shared modules
from realityscripts import shared

class CheckKitTemplates(shared.Application):

    def __init__(self, path: str):
        super().__init__(path, "objects", "kits")
        self.file_paths = set()
    
    def __call__(self):
        # Accumulate variants found from the repo
        for root, _, files, in os.walk(self.path):
            for file in files:
                if file == "variants.inc":
                    dir_path = os.path.realpath(root)
                    file_path = os.path.join(dir_path, file)
                    self.file_paths.add(file_path)
        # Evaluate the fetched variants
        for path in self.file_paths:
            self.search_variants(path)
        print("Finished processing objects")
    
    def search_variants(self, path: str):
        """
        1. Fetches for individual variants within the given variant file
        2. Checks each variant for missing pre-allocated objects
        """
        faction = path.split('\\')[-2]
        with open(path, "r") as file:
            variants = re.findall('("\w+"|else\b)(.*?)(?=else|$)', file.read(), re.DOTALL)
            for variant, kits in variants:
                self.check_kits(faction, variant, kits)
    
    def check_kits(self, faction: str, variant: str, kits: iter):
        # Initialize values
        k_loaded = set()
        k_allocated = set()

        # Allocate kits from the variant runs and preloaded
        PATTERN_ALLOCATED = re.compile('(?:ObjectTemplate\.setObjectTemplate \d) (\w+)')
        PATTERN__LOADED = re.compile('(?:ObjectTemplate.create Kit) (\w+)')
        for path in re.findall('run (.*?\.tweak)', kits):
            file_path = os.path.join(self.path, faction, path)
            with open(file_path, "r") as file:
                if "preload" in path:
                    kits = re.findall(PATTERN_ALLOCATED, file.read())
                    k_loaded.update(kits)
                else:
                    kits = re.findall(PATTERN__LOADED, file.read())
                    k_allocated.update(kits)

        # Calculate the differences between the two
        k_missing = k_loaded - k_allocated
        if len(k_missing) == 0:
            print(f'{variant}: no missing kits')
        else:
            print(f'{variant}: {k_missing}')
