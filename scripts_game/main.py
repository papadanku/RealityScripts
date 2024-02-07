"""
Scripts to process files in Project Reality: BF2
Author: [R-DEV]papadanku
"""

# Import shared modules
from realityscripts.ai import FindAITemplates
from realityscripts.kits import CheckKitTemplates
from realityscripts.shared import Application


def get_user_app():
    console_strings = [
        "\n Do you want to",
        "\t 1: Find AI Templates",
        "\t 2: Check Preallocated Kits",
        "",
    ]

    return int(input("\n".join(console_strings)))


def main():
    repo_path = input("Insert pr_repo path: ")
    user_app = get_user_app()

    app = Application('', '')
    if user_app == 1:
        app = FindAITemplates(repo_path)
    elif user_app == 2:
        app = CheckKitTemplates(repo_path)
    app()


if __name__ == "__main__":
    main()
