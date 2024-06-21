from lxml import etree
import re
from bs4 import BeautifulSoup
# style guide: capital letters for tags
def xml_builder(soup,visualize=False):
    """Visualize opens chrome tab with the colored soup object"""
    # find part I-IV start point (this may be tricky)
    # for each section construct tree
    root = etree.Element("root")

    header_tags = soup.find_all(attrs={'class': 'header'})



    part_tag_dict = {}
    for tag in header_tags:
        if re.search(r'^part\s+(i|ii|iii|iv)$', tag.text, re.IGNORECASE):
            part_tag_dict[re.sub(r'\n',' ',tag.text.strip()).upper().replace(" ","_")] = tag


    for key in part_tag_dict.keys():
        part = etree.SubElement(root, key)
        root.append(part)
    
    print(etree.tostring(root, pretty_print=True))


    