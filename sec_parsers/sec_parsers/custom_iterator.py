from lxml import etree
from typing import Optional, Iterator, Tuple
from sec_parsers.xml_helper import get_text, get_all_text
from sec_parsers.experimental_parsers import SEC10KParser
from sec_parsers import Filing
from time import time

class CustomBodyIterator:
    def __init__(self, root: etree._Element):
        self.root = root
        self.body = root.find('.//body')
        if self.body is None:
            raise ValueError("No <body> tag found in the document")

    def iter(self) -> Iterator[Tuple[etree._Element, Optional[etree._Element]]]:
        stack = [(self.body, None)]
        
        while stack:
            current, last_body_ancestor = stack.pop(0)
            
            yield current, last_body_ancestor
            
            for child in reversed(list(current)):
                if child.tag == 'body':
                    continue  # Skip nested body tags if any
                stack.insert(0, (child, current if current != self.body else last_body_ancestor))

def custom_iter(root: etree._Element) -> Iterator[Tuple[etree._Element, Optional[etree._Element]]]:
    return CustomBodyIterator(root).iter()


with open('../../Data/10K/1606_CORP.-1877461-0001477932-24-002182.html', 'r') as f:
    html = f.read()

filing = Filing(html)
root = filing.html

s = time()
tags = []
for element, last_body_ancestor in custom_iter(root):
    tags.append(element.tag)
print(time() - s)

s = time()
tags2 = []
for elem in root.iter():
    tags2.append(elem.tag)
print(time() - s)

print(len(tags), len(tags2))
