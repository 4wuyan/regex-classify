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

Use `-i` and `-o` to specify the input folder and the output folder respectively,
the default being the current working directory.

`-d` tells what the directory name looks like; the default value is `\1`.

`-f` specifies the new filename;
the default the value is group 0, i.e. the entire pattern, i.e. the original filename.
So it's not needed unless you want to rename the file.

## Examples

### Basic classification with a substring in the filename

#### Before
```
./A000VOI123ZH_00.pdf
./E100PIN105ZH_00.pdf
./classify.py
```

#### Command
```bash
python classify.py '....(......).....\.pdf'
```

#### After
```
./VOI123/A000VOI123ZH_00.pdf
./PIN105/E100PIN105ZH_00.pdf
./classify.py
```

### Capture multiple extensions

#### Before
```
./A000VOI123ZH_00.pdf
./E100PIN105ZH_00.docx
./classify.py
```

#### Command
```bash
python classify.py '....(......).....\.(pdf|docx)'
```

#### After
```
./VOI123/A000VOI123ZH_00.pdf
./PIN105/E100PIN105ZH_00.docx
./classify.py
```

### With renaming

#### Before
```
./A000VOI123ZH_00.pdf
./E100PIN105ZH.00.pdf
./classify.py
```

#### Command
```bash
python classify.py '(....(......)..).(..\.pdf)' -d '\2' -f '\1_\3'
```

#### After
```
./VOI123/A000VOI123ZH_00.pdf
./PIN105/E100PIN105ZH_00.pdf
./classify.py
```

### Multi-level classification

#### Before
```
'./bill smith'
'./amy smith'
'./tom smith'
'./bill gates'
'./sarah gates'
./classify.py
```

#### Command
```bash
python classify.py '(\w+) (\w+)' -d '\2/\1' -f '\1-\2'
```

#### After
```
./smith/bill/bill-smith
./smith/amy/amy-smith
./smith/tom/tom-smith
./gates/bill/bill-gates
./gates/sarah/sarah-gates
./classify.py
```

## Requirements

f-string and pathlib are used. Make sure your Python supports them.

Tests utilize pytest.
