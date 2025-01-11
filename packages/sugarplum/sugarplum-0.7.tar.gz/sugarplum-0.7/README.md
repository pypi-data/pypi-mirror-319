# sugarplum

[![PyPI - Version](https://img.shields.io/pypi/v/sugarplum.svg)](https://pypi.org/project/sugarplum)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sugarplum.svg)](https://pypi.org/project/sugarplum)

-----

Sugarplum is a library for managing inputs (both regular and test inputs) for Advent of Code puzzles.


## Why sugarplum

The creators of Advent of Code have asked that inputs not be shared, including test
inputs (see the links below). However, it can be helpful to not have to download
the puzzle inputs each time switching computers, or to have the test inputs stored for
running unit tests. That is where sugarplum comes in. It allows you to have a seperate 
directory, most likely a private repo, where these are stored, but easily retrieve them
for use in puzzle solutions and tests.

https://www.reddit.com/r/adventofcode/wiki/faqs/copyright/inputs/

https://www.reddit.com/r/adventofcode/comments/zh2hk0/comment/iznly9w/?context=3

## Installation

```console
pip install sugarplum
```

## Usage

The environment variable "SUGARPLUM_BASE_PATH" must be set to the base path of the 
directory where the inputs reside. At the moment, sugarplum is opinionated, expecting a
specific file structure and file names. It expects the directory structure to be one of
YYYY/DD.

Within that structure, it expects a file named input.txt for solution input, and a file 
named tests.yaml for test data. For more information on how to format the test data file,
see the next subsection.

To import your input data:

```python
from sugarplum import get_input_data

get_input_data(YYYY, DD)
```

To import your test data:

```python
from sugarplum import get_test_data

get_test_data(YYYY, DD, tag)
```

All test data is returned as a named tuple containing the keys "data" and "answer".

### tests.yaml

Sugarplum expectes the test data and answers to be stored in a YAML file named tests.yaml.
Your test file should be organzied using tags, which are top level keys. This allows you
to have multiple test data and answer combinations. For example, if you had three tests,
one for parsing, one for part 1, and one for part 2, your test file might look like the
following.

    parsing:
        data: LongInputString
        answer: 42
    part_1:
        data: part-1-data
        answer: 15
    part_2:
        data: part-2-data
        answer: 63

Because YAML allows complex data types, data within tests.yaml can be entered under tags
in one of three ways. It can be entered as a key-value pair, a key-list, or as a list of
key-value pairs. If it is entered as key-list, then the list is joined together into one
string as a multi-line string using \n as the join character.

**Key:Value pairs**

    tag:
        data: Your data here
        answer: 42

This will be returned as ("Your data here", 42)

**Key-List**

    tag:
        data:
            - one
            - two
            - three
        answer: 42

This will be returned as ("one\ntwo\nthree", 42)

**List of Key-Value pairs**

    tag:
        - data: something
          answer: 12
        - data: something else
          answer: 63

This will be returned as [("something", 12), ("something else", 63)]