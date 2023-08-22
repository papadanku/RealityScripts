
"""
Scripts to process files in Project Reality: BF2
Author: [R-DEV]papadanku
"""

# Import shared modules
from realityscripts import ai
from realityscripts import kits

def main():
    try:
        path = input("Insert repo path: ")
    except:
        print("Not a valid path")
    
    console = """
    Do you want to:
        [1]: Find AI Templates
        [2]: Check Kit Templates
    """
    user_input = input(console)
    print(user_input)


if __name__ == "__main__":
    main()
