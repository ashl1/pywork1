#!/usr/bin/env python3

from argparse import ArgumentParser
from pyquery import PyQuery
from lxml import etree

ATTRIBUTE_NAME = 'value2'

parser = ArgumentParser('Get average of all XML nodes'' attribute "value2"')
parser.add_argument('input', nargs=1, help='Absolute or relative path to the input XML file')
input_filename = parser.parse_args().input[0]

# cannot open or parse?
xml = PyQuery(filename=input_filename)

nodes = xml('[' + ATTRIBUTE_NAME + ']')

# ValueError: "cannot parse XML" or "ATTRIBUTE_NAME cannot be parsed as float"
avg = sum(float(node.get(ATTRIBUTE_NAME)) for node in nodes) / float(len(nodes))

print(avg)
