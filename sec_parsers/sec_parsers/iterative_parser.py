from sec_parsers.xml_helper import get_text, get_all_text
from sec_parsers.experimental_parsers import SEC10KParser
from sec_parsers import Filing
from time import time
from lxml import etree
from xml_helper import open_tree
from sec_parsers.cleaning import clean_title, is_string_in_middle

# Rewriting parser with iterative approach for better performance
# Should parse and convert to XML tree in one go
# estimated change in performance: ~.1s per file probably ambitious

# think about weird string handling due to nested elements and tails
# need something to keep track of parent, so as to modify parent's tail

# hidden css handling

# root = None # WIP
# body = root.find('body') # WIP

# need correct way to handle original elem

# I think we have to go with recursion.
# select children, process children 1x1

with open('../../Data/10K/1606_CORP.-1877461-0001477932-24-002182.html', 'r') as f:
    html = f.read()

filing = Filing(html)
filing.parse()
filing.visualize()
print(filing.get_title_tree())