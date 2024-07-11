from sec_parsers import download_sec_filing, set_headers, Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from sec_parsers.style_detection import detect_table
import pandas as pd
from lxml import etree


#1.
# fix item 7
with open('gencorp10k.html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = Parser(html)
# text = 'Financial Condition and Results of Operations'
# matching_elements = parser.html.xpath(f"//*[contains(text(), '{text}')]")
# table=matching_elements[4].getparent().getparent().getparent().getparent().getparent()
#recursive_parse(parser.html)
#table.xpath('.//*[@parsing_string]')
#element.xpath("./ancestor::table")

#relative_parsing(parser.html)
parser.parse()
parser.visualize()
#parser.save_csv('gencorp10k.csv')
#parser.save_xml('gencorp10k.xml')

#2.
# with open('ROANOKE ELECTRIC STEEL CORPORATION.html', 'r', encoding='utf-8') as f:
#     html = f.read()
#     html = html.encode('ascii')

# parser = Parser(html)
# parser.parse()
# parser.visualize()
# parser.save_csv('roanoke.csv')
# parser.save_xml('roanoke.xml')

#4.
# with open('GALAXY NEXT GENERATION, INC..html', 'r', encoding='utf-8') as f:
#     html = f.read()
#     html = html.encode('ascii')

# parser = Parser(html)
# parser.parse()
# parser.visualize()
# parser.save_csv('galaxy_next_generation.csv')
# parser.save_xml('galaxy_next_generation.xml')