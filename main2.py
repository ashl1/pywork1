#!/usr/bin/env python3

from argparse import ArgumentParser
import csv
import json
from operator import itemgetter
from os import path
from tempfile import TemporaryDirectory
from uuid import UUID
from zipfile import ZipFile

JSON_FILENAME = 'data.json'
OUT_FILENAME_GUIDS = 'guids.csv'
OUT_FILENAME_OTHERS = 'others.csv'

############## FUNCTIONS

def is_uuid(string):
    try:
        UUID(string)
    except ValueError:
        return False
    return True

def writeCSV(csv_filename, table):
    with open(csv_filename, 'w', newline='', encoding='utf_8_sig') as f:
        wr = csv.DictWriter(f, fieldnames=['name', 'str', 'value'], delimiter=';')
        wr.writeheader()
        for row in table:
            wr.writerow(row)

############## PROGRAM

parser = ArgumentParser('Get average of all XML nodes'' attribute "value2"')
parser.add_argument('input', nargs=1,
                    help='Absolute or relative path to the input ZIP-archive with JSON files')
parser.add_argument('output', nargs=1,
                    help='Absolute or relative path to the output ZIP-archive with JSON files')

input_filename = parser.parse_args().input[0]
output_filename = parser.parse_args().output[0]

guids = []
others = []
with ZipFile(input_filename, 'r') as z:
    dirs = frozenset([dir_[:-1] for dir_ in z.namelist() if dir_[-1]=='/'])

    for dir_ in dirs:
        json_content = z.read(dir_ + '/' + JSON_FILENAME).decode()
        content = json.loads(json_content)
        item = {'name': dir_, 'str': content['str'], 'value': content['value']}
        if is_uuid(dir_):
            guids.append(item)
        else:
            others.append(item)

    guids = sorted(guids, key=itemgetter('str'))
    guids = sorted(guids, key=itemgetter('value'))

    others = sorted(others, key=itemgetter('name'))

with TemporaryDirectory() as td:
    guids_filename = path.join(td, OUT_FILENAME_GUIDS)
    others_filename = path.join(td, OUT_FILENAME_OTHERS)

    writeCSV(guids_filename, guids)
    writeCSV(others_filename, others)

    with ZipFile(output_filename, 'w') as z:
        z.write(guids_filename, OUT_FILENAME_GUIDS)
        z.write(others_filename, OUT_FILENAME_OTHERS)

print('Done')
