from sec_parsers.xml_helper import get_text, get_all_text
from sec_parsers.experimental_parsers import SEC10KParser
from sec_parsers import Filing
from time import time
from lxml import etree
from xml_helper import open_tree

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
parser = SEC10KParser()


s = time()
element_style = ''
string_style = ''

flag = True
orig_elem = None

# fix ix nonumeric issue with assigning elements - WEIRD parsing string returns
# add relative parsing
# add xml tree construction
s = time()
for event, elem in etree.iterwalk(filing.html, events=('start', 'end')):
    if event == 'start':
        if flag:
            result, parsing_rule = parser.detect_style_from_element(elem)
            if parsing_rule == 'return':
                element_style = result
                orig_elem = elem
                flag = False
                continue
            elif result != '':
                if orig_elem is None:
                    orig_elem = elem

                element_style += result

            if string_style == '':
                string = get_all_text(elem) # need something to check if string already ran...., e.g. emphasis capitalization should happen once.
                result, parsing_rule = parser.detect_style_from_string(string)
                if parsing_rule == 'return':
                    string_style = result
                    orig_elem = elem
                    flag = False
                    continue
                elif result != '':
                    if orig_elem is None:
                        orig_elem = elem

                    string_style += result
        else:
            pass # iterate through file without parsing

    elif event == 'end':
        if orig_elem is not None:
            if elem == orig_elem:
                parsing_string = element_style + string_style
                orig_elem.attrib['parsing_string'] = parsing_string

                flag = True
                orig_elem = None
                string_style = ''
                element_style = ''

parser.clean_parse(filing.html)
print(f"Parsed in {time()-s:.2f}s")
filing.visualize()