# Note: this file is for me to debug and test code snippets. It is not part of the final project.
import bs4

from download import download_sec_filing

html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm')

soup = bs4.BeautifulSoup(html, 'html.parser')

from parsers import parse_10k

tree = parse_10k(html)

from xml_helper import print_xml_structure, get_text_from_node
print_xml_structure(tree)

# # save xml to file
import xml.etree.ElementTree as ET
tree.write('aapl-20200926.xml', encoding='utf-8-sig')