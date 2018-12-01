import re
import argparse
import os
import shutil
import sys
import logging


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default=os.getcwd(), help="source directory")
    parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help="target directory")
    parser.add_argument('regex', type=str, help="regular expression for matching")
    parser.add_argument('-d', '--directory', type=str, default=r'\g<1>', help="regex for new directory names")
    parser.add_argument('-f', '--file', type=str, default=r'\g<0>', help="regex for new filename")

    args = parser.parse_args()
    return args


class File:
    def __init__(self, full_path):
        self._full_path = full_path

    @property
    def filename(self):
        return os.path.basename(self._full_path)

    @property
    def directory(self):
        return os.path.dirname(self._full_path)

    @property
    def absolute_path(self):
        return self._full_path

    def move_to(self, target_path):
        target_path = os.path.abspath(target_path)
        self._full_path = shutil.move(self._full_path, target_path)


def main():
    args = parse_arguments()

    source_directory = args.input
    target_directory = args.output
    matching_pattern = re.compile(args.regex)
    directory_regex = args.directory
    file_regex = args.file

    matching_files = []
    for root, _subdirectories, files in os.walk(source_directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            if matching_pattern.match(filename) is None:
                logging.info(f'{full_path} is ignored.')
            else:
                matching_files.append(File(full_path))

    for file in matching_files:
        new_filename = matching_pattern.sub(file_regex, file.filename)
        folder_name = matching_pattern.sub(directory_regex, file.filename)
        destination_directory = os.path.join(target_directory, folder_name)

        if not os.path.isdir(destination_directory):
            os.makedirs(destination_directory)

        target_path = os.path.join(destination_directory, new_filename)
        if os.path.isfile(target_path):
            logging.warning(f'{target_path} already exists! {file.absolute_path} not moved.')
        else:
            file.move_to(target_path)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    main()
