from sec_parsers import Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *
from lxml import etree
import os

files = os.listdir(dir_10k)[0:1]
for count,file in enumerate(files):
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    filing = Parser(html)

# WIP, trying to make get_elements_between_elements more efficient
# i think we need to learn how to be wizards at xpath
def iter_tree(start_element, end_element):
    """WIP"""
    following = start_element.xpath('following') # this should speed stuff up, but now we have issue of grabbing too much

html = filing.html

start_element = html.getchildren()[1].getchildren()[-200]
end_element = html.getchildren()[1].getchildren()[-100]
following = start_element.xpath('following::*')

text1 = '\n'.join([item.text for item in following if item.text is not None])
