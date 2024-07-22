from sec_parsers.xml_helper import get_text, get_all_text
from sec_parsers import Filing
from lxml import etree
import os
from global_vars import *
from time import time
import re
file = os.listdir(dir_10k)[0]
with open(dir_10k + file, 'r', encoding='utf-8') as f:
    html = f.read()


filing = Filing(html)

body = filing.html.xpath('//body')[0]
# Find all elements with style containing 'display:none'
display_none_elements = body.xpath("//*[contains(@style, 'display:none')]")

# Remove each of these elements
for element in display_none_elements:
    element.getparent().remove(element)

# figure out how to keep track of parents
count = 0

# keeps track of style until text, then resets
parsing_string = ''

for elem in body.iter():
    if elem.text is None:
        parsing_string += elem.tag
    else:
        parsing_string += elem.text
        parsing_string = re.sub('\n','',parsing_string)
        print(parsing_string)
        parsing_string = ''
        count +=1

    if count > 90:
        break
    
    

    