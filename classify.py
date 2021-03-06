import re
import argparse
from pathlib import Path
import sys
import logging


def _parse_arguments(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=Path, default=Path.cwd(), help="source directory")
    parser.add_argument('-o', '--output', type=Path, default=Path.cwd(), help="target directory")
    parser.add_argument('regex', type=str, help="regular expression for matching")
    parser.add_argument('-d', '--directory', type=str, default=r'\g<1>', help="regex for new directory names")
    parser.add_argument('-f', '--file', type=str, default=r'\g<0>', help="regex for new filename")

    arguments = parser.parse_args(args) if args else parser.parse_args()
    return arguments


def main(*args):
    arguments = _parse_arguments(*args)

    source_directory = arguments.input.resolve()
    target_directory = arguments.output.resolve()
    matching_pattern = re.compile(arguments.regex)
    directory_regex = arguments.directory
    file_regex = arguments.file

    matching_paths = []
    for path in source_directory.glob(r'**/*'):
        if path.is_file():
            if matching_pattern.match(path.name) is None:  # path.name is filename
                logging.warning(f'{path} is ignored.')
            else:
                matching_paths.append(path)

    for path in matching_paths:
        filename = path.name
        new_filename = matching_pattern.sub(file_regex, filename)
        folder_name = matching_pattern.sub(directory_regex, filename)

        folder_path = target_directory / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        new_path = folder_path / new_filename
        if new_path.is_file():
            logging.warning(f'{new_path} already exists! {path} not moved.')
        else:
            path.rename(new_path)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    main()
