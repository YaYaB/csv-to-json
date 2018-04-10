# Csv to json
> Simply transform a csv to json


This tool helps you create a json from a csv. It infers json's structure based on csv's columns and a given delimiter.
For instance if the columns of the csv are the following:
```
team_captain, team_defend, team_str, card_yellow, card_red
```

Given the delimiter equals to *_*, the json's structure would be:
```
{
    'team':{
        'captain':,
        'defend':,
        'str' :
    },
    'card':{
        'yellow':,
        'red':
    }
}
```


## Installation

OS X, Linux & Windows:
No specific requirements except python3 (3.4 and later).

```sh
pip install git+https://github.com/YaYaB/csv-to-json
```


## Usage example

```sh
usage: Create json file from csv by infering json'structure using a delimiter inside csv's columns.
       [-h] [--csv CSV] [--json JSON] [--delimiter DELIMITER]
       [--config CONFIG] [--cols_delimiter COLS_DELIMITER]
       [--max_docs MAX_DOCS] [--per_line] [--infer_types] [--keep]

optional arguments:
  -h, --help            show this help message and exit
  --csv CSV             Set path to csv file as input
  --json JSON           Set path to json file as output
  --delimiter DELIMITER
                        Set delimiter used to infer json's structure
                        (default='_')
  --config CONFIG       Set path to json file containing data type information
                        and or default value(default='None', optional and
                        precise column type)
  --cols_delimiter COLS_DELIMITER
                        Set delimiter of the csv (default=',')
  --max_docs MAX_DOCS   Set max number of documents in a json file, several
                        will be created if necessary (default='-1' means
                        single output file)
  --per_line            Dump a file containing one json per line. Careful the
                        output is not a correct json (default='False')
  --infer_types         Infer data type based on its value: float, list and
                        date are supported. Carefull, 'config' will override
                        it if specified. (default='False')
  --keep                Keep fields with empty values replaced by null instead
                        of ignoring them (default='True')

```sh

Many possible are given.
Please refer to [here](https://github.com/YaYaB/csv-to-json/examples) for examples.



## Meta

YaYaB

Distributed under the Apache license v2.0. See ``LICENSE`` for more information.

[https://github.com/YaYaB/csv-to-json](https://github.com/YaYaB/csv-to-json)
