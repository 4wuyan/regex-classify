# regex-classify

Classify files with regex.

## Usage

```
$ python classify.py --help
usage: classify.py [-h] [-i INPUT] [-o OUTPUT] [-d DIRECTORY] [-f FILE] regex

positional arguments:
  regex                 regular expression for matching

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        source directory
  -o OUTPUT, --output OUTPUT
                        target directory
  -d DIRECTORY, --directory DIRECTORY
                        regex for new directory names
  -f FILE, --file FILE  regex for new filename
```

Use `-i` and `-o` to specify the input folder and output folder respectively,
the default being the current working directory.

`-d` tells what the directory name looks like; the default value is `\1`.

`-f` specifies the new filename;
the default the value is group 0, i.e. the entire pattern, i.e. the original filename.
So it's not needed unless you want to rename the file.

## Examples

### Basic classification with a substring in the filename

#### Before
```
pass
```

### Capture multiple extensions

### With renaming

### Multi-level classification

## Requirements

f-string and pathlib are used. Make sure your Python supports them.

Tests utilize pytest.
