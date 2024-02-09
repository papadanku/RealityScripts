"""
Library to process objects
"""

# Import Python modules
import glob
import os
import re

# Import shared modules
from realityscripts import shared


class CheckKitTemplates(shared.Application):

    def __init__(self, repo_path):
        super().__init__(repo_path, "objects/kits")
        self.file_paths = []

    def __call__(self):
        """
        Accumulate and evaluate variants found from the repo
        """
        self.file_paths = glob.glob("/".join([self.path, "*", "variants.inc"]))
        for path in self.file_paths:
            self.search_variants(path)
        print("Finished processing objects")

    def search_variants(self, path):
        """
        1. Fetches for individual variants within the given variant file
        2. Checks each variant for missing pre-allocated objects
        """

        faction = path.split("\\")[-2]
        with open(path, "r") as file:
            variants = re.findall(r'("\w+"|else\b)(.*?)(?=else|$)', file.read(), re.DOTALL)
            for variant, kits in variants:
                self.check_kit_templates(faction, variant, kits)

    def check_kit_templates(self, faction, variant, kit_files):
        """
        Checks every kitTemplate's .tweak files
        """

        PATTERN_ALLOCATED = re.compile(r'ObjectTemplate\.setObjectTemplate \d (\w+)')
        PATTERN_LOADED = re.compile(r'ObjectTemplate\.create Kit (\w+)')

        # Initialize kit collections
        kits = {"loaded": set(), "allocated": set()}

        # Allocate kits from the variant runs and preloaded
        for path in re.findall(r'run (.*?\.tweak)', kit_files):
            file_path = os.path.join(self.path, faction, path)
            with open(file_path, "r") as file:
                if "preload" in path:
                    kit_templates = re.findall(PATTERN_ALLOCATED, file.read())
                    kits["allocated"].update(kit_templates)
                else:
                    kit_templates = re.findall(PATTERN_LOADED, file.read())
                    kits["loaded"].update(kit_templates)

        # Calculate the differences between the two
        k_missing = kits["loaded"] - kits["allocated"]
        if len(k_missing) == 0:
            print(f"{variant}: no missing kits")
        else:
            print(f"{variant}: {k_missing}")
