from sec_parsers import download_sec_filing, set_headers, Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from sec_parsers.style_detection import detect_table
import pandas as pd
from lxml import etree


#1. Gencorp
with open('gencorp10k.html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = Parser(html)

parser.parse()
parser.visualize()
#parser.save_csv('gencorp10k.csv')
parser.save_xml('gencorp10k.xml')

#2.
with open('ROANOKE ELECTRIC STEEL CORPORATION.html', 'r', encoding='utf-8') as f:
    html = f.read()
parser = Parser(html)
parser.parse()
parser.visualize()
#parser.save_csv('roanoke.csv')
parser.save_xml('roanoke.xml')

#4.
with open('GALAXY NEXT GENERATION, INC..html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = Parser(html)
parser.parse()
parser.visualize()
parser.save_csv('galaxy_next_generation.csv')
parser.save_xml('galaxy_next_generation.xml')