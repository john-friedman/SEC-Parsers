from bs4 import BeautifulSoup
import re
import pandas as pd
import xml.etree.cElementTree as ET
from bs4 import NavigableString, Tag

# untested
def get_elements_between_two_elements(elem1, elem2):
    """Get all elements between two beautiful soup tags. """
    end_bool = False
    elements = []

    item = elem1.next
    while not end_bool:
        if item == elem2:
            end_bool = True
        else:
            if isinstance(item, Tag):
                elements.append(item)
        # go to next item
        item = item.next
    return elements

# tested
# add cleaning later
def get_text_between_two_elements(elem1, elem2):
    """Get the text between two beautiful soup tags. """
    end_bool = False
    text = ''

    item = elem1.next
    while not end_bool:
        if item == elem2:
            end_bool = True
        else:
            if isinstance(item, NavigableString):
                    # apply cleaning
                    text += item
        # go to next item
        item = item.next
    return text


# works for now, but should do robustness checks - easy to catch
def detect_table_of_contents(element):
    """Detects if a table is likely to be a table of contents."""
    # get number of links
    links = element.find_all('a')
    if len(links) > 5:
        return True

# will need a bunch of work. This is our workhorse.
def handle_table_of_contents(soup):
    """Handles the table of contents in a sec 10k"""
    tables = soup.findAll('table')
    table_of_contents_detected = False
    for table in tables:
        if detect_table_of_contents(table):
            table_of_contents_detected = True
            break

    if not table_of_contents_detected:
        raise ValueError('Table of contents not detected')
    
def detect_subheadings(elements):
    subheadings_element_list = ''
    return subheadings_element_list

# untested, code sketch
# with some work should return detailed xml tree
# add visualizer option? -yes
def parse_10k(html):
    soup = BeautifulSoup(html, 'html.parser')    

    # read table of contents
    # I think we want to change this to a list of dictionaries
    #df = handle_table_of_contents(soup)
    # maybe {name: 'part i', href: '#parti', items : [{name: 'item 1', href: '#item1'}, {name: 'item 2', href: '#item2'}]}
    # need to do cleaning here too
    toc_dict = handle_table_of_contents(soup)

    root = ET.Element("root")

    parts_list = toc_dict['parts']
    # -1 explanation remember to handle end tag
    for part_idx,_ in enumerate(parts_list)[:-1]:
        # [1:] to skip the # in the href
        part = parts_list[part_idx]
        next_part = parts_list[part_idx+1]

        part_id = part['href'][1:]
        next_part_id = next_part['href'][1:]

        part_name = part['name']
        next_part_name = next_part['name']

        xml_part_element = ET.SubElement(root, part_name)

        # find elements using href
        part_elem = soup.find(id=part_id)
        if part_elem is None:
            # sometimes links have names instead of id
            part_elem = soup.find('a', {'name': part_id})

        next_part_elem = soup.find(id=next_part_id)
        if next_part_elem is None:
            next_part_elem = soup.find('a', {'name': next_part_id})

        # handle items in part
        items_list = part['items']
        for item_idx, _ in enumerate(items_list):
            item = items_list[item_idx]
            next_item = items_list[item_idx+1]

            item_id = item['href'][1:]
            next_item_id = next_item['href'][1:]

            item_name = item['name']
            next_item_name = next_item['name']

            item_elem = soup.find(id=item_id)
            if item_elem is None:
                item_elem = soup.find('a', {'name': item_id})
            
            next_item_elem = soup.find(id=next_item_id)
            if next_item_elem is None:
                next_item_elem = soup.find('a', {'name': next_item_id})

            xml_item_element = ET.SubElement(part, item_name)

            # detect subheadings between item and next_item
            elements_between = get_elements_between_two_elements(item_elem, next_item_elem)
            subheadings_element_list = detect_subheadings(elements_between)

            # now we iterate through the subheadings elements and get the text between them
            for sub_idx, _ in enumerate(subheadings_element_list)[:-1]:
                # find subheading name and clean
                subheading_name = subheadings_element_list[sub_idx].text

                subsection_text = get_text_between_two_elements(subheadings_element_list[sub_idx], subheadings_element_list[sub_idx+1])

                # add to tree
                xml_subsection_element = ET.SubElement(xml_item_element, subheading_name)
                xml_subsection_element.text = subsection_text