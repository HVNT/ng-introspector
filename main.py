import string
import sys
import os

def traverse(dir_path, prefix):
    directory = os.listdir(dir_path)
    target_files = []
    # recursive check
    for file_name in directory:
        if prefix in file_name:
            target_files.append(file_name)
    return target_files


def main():
    dir_path = sys.argv[1]  # relative path to directory that contains ng project to be introspected


if __name__ == "__main__":
    main()
