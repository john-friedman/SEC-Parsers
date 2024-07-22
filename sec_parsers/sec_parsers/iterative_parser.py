from sec_parsers.xml_helper import get_text, get_all_text
from sec_parsers.experimental_parsers import SEC10KParser
from sec_parsers import Filing
from time import time


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

with open('../../Data/10K/1606_CORP.-1877461-0001477932-24-002182.html', 'r') as f:
    html = f.read()

filing = Filing(html)
parser = SEC10KParser()


s = time()
parsing_string = '' # keep track of parsing string
flag = True
orig_elem = None

for elem in filing.html.iter():
    if elem.tag in ['html', 'head', 'body']:
        continue

    if flag:
        # element detection
        result, parsing_rule = parser.detect_style_from_element(elem)
        if parsing_rule == 'return':
            parsing_string = result
            flag = False
            orig_elem = elem
            continue

        else:
            if orig_elem is None:
                orig_elem = elem

            parsing_string += result

        # string detection
        string = get_all_text(elem)
        result, parsing_rule = parser.detect_style_from_string(string)
        if parsing_rule == 'return':
            parsing_string = result
            flag = False
            orig_elem = elem
            continue

        else:
            if orig_elem is None:
                orig_elem = elem

            parsing_string += result


    if elem.getnext() is None:
        if parsing_string != '':
            parsing_list = list(set(parsing_string.split(';')))
            parsing_list = [x for x in parsing_list if x != '']
            parsing_string = ';'.join(parsing_list) +';'
            orig_elem.attrib['parsing_string'] = parsing_string

            parsing_string = ''
            flag = True
            orig_elem = None

    # use has text / tail to determine if we are at end? or maybe has children? to reset parsing string
    # how to skip e.g. display none - bypass with removal, remember to only subset body elem

# HMMM
# we may want custom elem iter, aka recursion again....
print(f"Time taken: {time() - s}")
parser.clean_parse(filing.html)
filing.visualize()