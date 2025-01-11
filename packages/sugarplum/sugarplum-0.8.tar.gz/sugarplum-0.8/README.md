# sugarplum

[![PyPI - Version](https://img.shields.io/pypi/v/sugarplum.svg)](https://pypi.org/project/sugarplum)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sugarplum.svg)](https://pypi.org/project/sugarplum)

-----

Sugarplum is a library for managing inputs (both regular and test inputs) for Advent of Code puzzles.


## Why sugarplum

The creator of Advent of Code haas asked that inputs, including test inputs, not be 
shared or published (see the links below for the original posts). Not sharing or
publishing them means keeping them out of any source control that is public facing. This
leads to the question of how to manage solution inputs, and any inputs used for testing.
Sugarplum aims to solve this problem by allowing the import of data stored outside of
the directories where solutionsand tests are stored. This way a seperate, private
repository, can be used to store any inputs and test data.

https://www.reddit.com/r/adventofcode/wiki/faqs/copyright/inputs/

https://www.reddit.com/r/adventofcode/comments/zh2hk0/comment/iznly9w/?context=3

## Installation

```console
pip install sugarplum
```

## Usage

Since the point of Sugarplum is to import data stored in a directory tree seperate from
the code requesting it, the base path of where that data is stored needs to be defined.
Sugarplum looks for an environment variable `SUGARPLUM_BASE_PATH` which, as the name
implies, holds the base path of the diretory tree where the inputs are stored.

Sugarplum is very opinionated about the structure of the directory tree where the data
is stored. It expects to have a top level directory that consists of sub-directories for
each year. Within those sub-directories it expects further sub-directories for each day.
The directories for the days should be zero-padded so that all directory names are two
digits long. Within the day directories, it expects specific file naming schemes.
Solution inputs must be stored within files named "input.txt". Test data must be 
stored in files named "tests.yaml". An example directory is shown below. See the test 
input section for how to structure the tests.yaml file.

```
- YourDataDirectory (This is what SUGARPLUM_BASE_PATH points to)
    - 2015
        - 01
            - input.txt
        - 14
            - input.txt
            - tests.yaml
    - 2021
        - 05
            - input.txt
            - tests.yaml
```

### Importing solution data

To import solution data, call the `get_input_data` function. The year and day must be 
passed as integers. The function will return a string, which will be the contents of 
input.txt.

```python
from sugarplum import get_input_data

data: str = get_input_data(YYYY, DD)
```

### Structuring test data

Test data is stored within tests.yaml. The file should contain top level keys, tags,
that are used to identify groupings of test data. Each file can have as many tags, and therefore subsets of data, as you would like. Under these keys test data can be 
structured in three ways. Each way depends on two pre-defined key names "data" and 
"answer".

1. A key/value pair
2. A key/value pair which has a list under the data key.
3. A list of key/value pairs.

For test data that is one-to-one, one data set/answer per test, a single data key and
answer key is used.

```
tag:
    data: "North Pole"
    answer: 42
```

Test data where the data consists of multiple lines of data can be listed as a list 
under the data key. As the example shows, empty lines are simply denoted by an empty
list item.

```
tag:
    data:
        - one
        - two
        -
        - three
    answer: 25
```

The data in the above list would be returned as "one\ntwo\n\nthree"

Data where there is a one-to-many relationship with one test being run over multiple
data sets, can be listed by a list of data/answer keys under the tag.

```
tag:
    - data: Santa Claus
      answer: 1
    - data: Kris Kringle
      answer: 2
```

The data in the above list would be returned as a list of TestData instances.

### Importing test data

To import test data, call the `get_test_data` function, passing in the year, day, and
tag to be used. The year and day must be an integer.

Test data is returned as either an instance of TestData or a list of TestData instances. TestData is a named tuple that uses the keys "data" and "answer".

```python
from sugarplum import get_test_data

test: TestData = get_test_data(2015, 1, "tag-name")

data: str = test.data
answer: int = test.answer

# Result would be TagData(data, answer)

test2: TestData = get_test_data(2015, 1, "multi-data-tag")

# Result would be [TagData(data1, answer1), TagData(data2, answer2), ...]

data1: str = test2[0].data
answer1: int = test2[0].answer
```