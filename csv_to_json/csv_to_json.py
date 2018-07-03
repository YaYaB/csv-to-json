import os
import sys
import argparse
import json
import csv
import collections
import copy
import ast
import datetime
import dateutil.parser


def get_args():
    """
        Get arguments of the program

        :return: arguments parsed
    """

    parser = argparse.ArgumentParser(
        "Create json file from csv by infering json'structure using a delimiter inside csv's columns."
    )
    parser.add_argument("--csv", type=str, help='Set path to csv file as input')
    parser.add_argument("--json", type=str, help='Set path to json file as output')
    parser.add_argument("--delimiter", type=str, default='_', help='Set delimiter used to infer json\'s structure (default=\'_\')')
    parser.add_argument("--config", type=str, default=None, help='Set path to json file containing data type information and or default value(default=\'None\', optional and precise column type)')    
    parser.add_argument("--cols_delimiter", type=str, default=',', help='Set delimiter of the csv (default=\',\')')
    parser.add_argument("--max_docs", type=int, default=-1, help='Set max number of documents in a json file, several will be created if necessary (default=\'-1\' means single output file)')    
    parser.add_argument("--per_line", action='store_true', default=False, help='Dump a file containing one json per line. Careful the output is not a correct json (default=\'False\')')
    parser.add_argument("--infer_types", action='store_true', default=False, help='Infer data type based on its value: float, list and date are supported. Carefull, \'config\' will override it if specified. (default=\'False\')')    
    parser.add_argument("--keep", action='store_true', default=False, help='Keep fields with empty values replaced by null instead of ignoring them (default=\'True\')')    
    args = parser.parse_args()
    return args


def infer_type(x):
    """
        Infer type of a string input.

        :param x: input as a string
        :return: return x cast to type infered or x itself if no type was infered
    """

    str_to_types = [ast.literal_eval,
                    int,
                    float,
                    lambda x: dateutil.parser.parse(x).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    str
                   ]
    for f in str_to_types:
        try:
            return f(x)
        except (ValueError, SyntaxError, TypeError):
            pass
    return x


def get_header_csv(csv_file, cols_delimiter):
    """
        Get header of a csv

        :param csv_file: path to the csv file
        :param cols_delimiter: delimiter between columns
        
        :return: header of csv as a list of strings
    """

    with open(csv_file, "r") as f:
        reader = csv.reader(f, delimiter=cols_delimiter)
        header_csv = next(reader)
    
    return header_csv


def create_jstruct(jstruct, elem_struct, val):
    """
        Create json structure (recursive function)

        :param jstruct: jstruct to update
        :param elem_struct: nested field represented as list
        :param val: value of the nested field        
        
        :return: json structure created (updated)
    """

    if len(elem_struct) == 1:
        jstruct[elem_struct[0]] = val
    else:
        elem = elem_struct.pop(0)
        if elem not in jstruct:
            jstruct[elem] = {}
        jstruct[elem] = create_jstruct(jstruct[elem], elem_struct, val)

    return jstruct


def create_json_structure(header_csv, delimiter):
    """
        Create json structure

        :param header_csv: header_csv that contains the futur json's fields
        :param delimiter: delimiter of the nested json      
        
        :return: json structure created
    """

    # Sort header of csv to find the hierarchy easier
    header_csv.sort()
    jstruct = {}
    for elem in header_csv:
        elem_struct = elem.split(delimiter)
        jstruct.update(create_jstruct(jstruct, elem_struct, {}))

    return jstruct


def update_jstruct(jstruct, elem_struct, val, keep):
    """
        Update json structure (recursive function)

        :param jstruct: jstruct to update
        :param elem_struct: nested field represented as list
        :param val: value of the nested field        
        :param keep: if true write None values instead of skipping them
        :return: json structure updated
    """

    if len(elem_struct) == 1:
        try:      
            if val == '':
                val = None
            if val == None and not keep:
                del jstruct[elem_struct[0]]
            else:
                jstruct[elem_struct[0]] = val

        except:
            print("  [ERR] Can not associate value ", val, "to field", elem_struct[0])
            jstruct[elem_struct[0]] = None
            pass
    else:  
        elem = elem_struct.pop(0)
        jstruct[elem] = update_jstruct(jstruct[elem], elem_struct, val, keep)

    return jstruct


def create_json_example(row, header_csv, jstruct, delimiter, keep, dic_types):
    """
        Create one json from one example

        :param row: row of a csv corresponding to example
        :param header_csv: header of the csv
        :param jstruct: json structure already created
        :param delimiter: delimiter of the nested json
        :param keep: if true write None values instead of skipping them
        :param dic_types: dictionarry containing type and default value of each field
        
        :return: json structure updated
    """

    for key in header_csv:
        key_struct = key.split(delimiter)
        if key in dic_types.keys():
            # if no value indicated set to default
            if row[key] == '' and 'default' in dic_types[key].keys():
                row[key] = dic_types[key]['default']
            else:
                try:
                    # Cast to indicated type
                    row[key] = dic_types[key]['type'](row[key])              
                except:
                    print("  [WARN] Can not parse ", row[key] , "to type", dic_types[key]['type'])
        jstruct.update(update_jstruct(jstruct, key_struct, row[key], keep))
    
    return jstruct


def create_json_from_csv(csv_file, delimiter, cols_delimiter, keep, dic_types, infer_types):
    """
        Create one json for a whole csv

        :param csv_file: path to csv file
        :param delimiter: delimiter of the nested json (delimiter inside a column)
        :param cols_delimiter: delimiter of the columns in the csv
        :param keep: if true write None values instead of skipping them
        :param dic_types: dictionarry containing type and default value of each field
        :param infer_types: if true, will try to infer_types of fields       
        
        :return: json content
    """

    # Get header of csv
    header_csv = get_header_csv(csv_file, cols_delimiter)

    # Create structure of json
    print('  [INFO] Creating json\'s structure')
    jstruct = create_json_structure(header_csv, delimiter)
    print(jstruct)
    # Read csv line by line and create list of json
    print('  [INFO] Filling json')    
    js_content = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=cols_delimiter)
        for row in reader:
            if infer_types:
                row = {x: infer_type(row[x]) for x in row}
            jexample = copy.deepcopy(jstruct)
            js_content.append(create_json_example(row, header_csv, jexample, delimiter, keep, dic_types))
    
    return js_content


def dump_json(json_file, json_doc, per_line):
    """
        Dump a json in one file

        :param json_file: path to output file wanted
        :param json_doc: json document 
        :param per_line: if true, write one json per line (specific format)   
        
    """

    with open(json_file, 'w') as jsf:
        if  per_line:
            jsf.write(
                '\n'.join(json.dumps(i) for i in json_doc)
            )
        else:
            jsf.write('[\n')            
            jsf.write(
                ',\n'.join(json.dumps(i) for i in json_doc)
            )
            jsf.write('\n]') 


def str_to_type(name_type):
    """
        Get type from string

        :param name_type: string containing name_type     
        
        :return: type or function to cast to specific type
    """
    if name_type == 'float' or name_type == 'Float':
        return float
    if name_type == 'bool':
        return bool
    if name_type == 'int':
        return int
    if name_type == 'list':
        return ast.literal_eval
    if name_type == 'date':
        return lambda x: dateutil.parser.parse(x).strftime('%Y-%m-%dT%H:%M:%SZ')
    if name_type == 'str':
        return str

   
    return None


def read_config(config):
    """
        Read config file containing information of type and default values of fields

        :param config: path to config file   
        
        :return: dictionary containing type and or default value for each field in the file
    """

    dic_types = json.load(open(config, 'r'))

    to_remove = []
    for attribute, value in dic_types.items():
        ls_val = value.keys()
        if 'type' in ls_val:
            val = value['type']
            value['type'] = str_to_type(val)
            none_type = False
            if not value['type']:
                none_type = True
                
        if not 'default' in ls_val and none_type:
            to_remove.append(attribute)
            value['type'] = val

    for to_rm in to_remove:
        print('  [WARN] Config for' , '\'' + to_rm + '\'', 'incorrect and ommitted: Type', '\'' + dic_types[to_rm]['type'] + '\'' , 'is not valid and no default value is indicated')        
        del dic_types[to_rm]
                
    return dic_types


def main():
    """
        Main function of the program
    """

    # Load arguments
    args = get_args()
    
    assert os.path.exists(args.csv), '  [ERR] File' + os.path.exists(args.csv) +'does not exist'

    print(args)
    try:
        dir_name = os.path.dirname(args.json)
        os.mkdir(dir_name)
        print('  [INFO] Creating', dir_name, 'directory')
    except:
        print('  [INFO] Directory', dir_name, 'already exists. Data will be replaced')
        pass

    if args.config:
        assert os.path.exists(args.config), '  [ERR] File' + os.path.exists(args.config) +'does not exist'
        dic_types = read_config(args.config)
    else:
        dic_types = {}
        
    # Create json
    json_doc = create_json_from_csv(args.csv, args.delimiter, args.cols_delimiter, args.keep, dic_types, args.infer_types)

    # Dump json into one file
    if args.max_docs == -1:
        dump_json(args.json, json_doc, args.per_line)

    # Dump json into several files
    else:
        base_name = '.'.join(args.json.split('.')[:-1])
        suf = 0
        while True:
            json_part = json_doc[:args.max_docs]
            dump_json(base_name + '_' + str(suf) + '.json', json_part, args.per_line)

            del json_doc[:args.max_docs]
            suf += 1

            if not json_doc:
                break
    print('  [INFO] Json{} successfully created and dumped'.format('s' if (args.max_docs != -1) else ''))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("  [ERR] Uncaught error waiting for scripts to finish")
        print(e)
        raise
