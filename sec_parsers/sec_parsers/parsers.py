from bs4 import BeautifulSoup
import re
import pandas as pd
import xml.etree.cElementTree as ET
from bs4 import NavigableString, Tag

from html_helper import get_elements_between_two_elements, get_text_between_two_elements, detect_subheadings, get_table_of_contents

#TODO we added support for part href being empty need to update here

# untested, code sketch
# with some work should return detailed xml tree
# add visualizer option? -yes
def parse_10k(html):
    soup = BeautifulSoup(html, 'html.parser')    

    toc_dict = get_table_of_contents(soup)

    root = ET.Element("root")

    parts_list = toc_dict['parts']
    for part_idx,_ in list(enumerate(parts_list)):
        part = parts_list[part_idx]
        # [1:] to skip the # in the href
        part_id = part['href'][1:]
        part_name = part['name']

        # find elements using href
        part_elem = soup.find(id=part_id)
        if part_elem is None:
            # sometimes links have names instead of id
            part_elem = soup.find('a', {'name': part_id})

        # handle last part
        if part_idx == len(parts_list) - 1:
            next_part_elem = None
        else:
            next_part = parts_list[part_idx+1]
            next_part_id = next_part['href'][1:]
            next_part_name = next_part['name']

            next_part_elem = soup.find(id=next_part_id)
            if next_part_elem is None:
                next_part_elem = soup.find('a', {'name': next_part_id})

        xml_part_element = ET.SubElement(root, part_name)
        items_list = part['items']
        for item_idx, _ in list(enumerate(items_list)):
            item = items_list[item_idx]
            item_id = item['href'][1:]
            item_name = item['name']
            item_desc = item['desc']

            item_elem = soup.find(id=item_id)
            if item_elem is None:
                item_elem = soup.find('a', {'name': item_id})

            # handle last item
            if item_idx == len(items_list) - 1:
                next_item_elem = None
            else:
                next_item = items_list[item_idx+1]
                next_item_id = next_item['href'][1:]
                next_item_name = next_item['name']

                next_item_elem = soup.find(id=next_item_id)
                if next_item_elem is None:
                    next_item_elem = soup.find('a', {'name': next_item_id})

            xml_item_element = ET.SubElement(xml_part_element, item_name, desc =item_desc)

            # detect subheadings between item and next_item
            elements_between = get_elements_between_two_elements(item_elem, next_item_elem)
            subheadings_element_list = detect_subheadings(elements_between)

            # inset item elem at the beginning and next_item elem at the end
            # we do this as there is often text between the item and the first subheading. This also helps in case there are no subheadings
            subheadings_element_list.insert(0, item_elem)
            subheadings_element_list.append(next_item_elem)

            # now we iterate through the subheadings elements and get the text between them
            # wow this is borked. go shopping and think about it
            for sub_idx, _ in list(enumerate(subheadings_element_list)):
                # stop before last element
                if sub_idx < len(subheadings_element_list) - 1:
                    if subheadings_element_list[sub_idx] is not None:
                        if sub_idx == 0:
                            subheading_name = 'subsection' # generic name
                        else:
                            # find subheading name and clean
                            subheading_name = subheadings_element_list[sub_idx].text

                        if sub_idx == len(subheadings_element_list) - 1:
                            # handle last subheading
                            subsection_text = get_text_between_two_elements(subheadings_element_list[sub_idx], None)

                            # add to tree
                            xml_subsection_element = ET.SubElement(xml_item_element, subheading_name)
                            xml_subsection_element.text = subsection_text
                        else:
                            subsection_text = get_text_between_two_elements(subheadings_element_list[sub_idx], subheadings_element_list[sub_idx+1])
                        
                            # add to tree
                            xml_subsection_element = ET.SubElement(xml_item_element, subheading_name)
                            xml_subsection_element.text = subsection_text




    tree = ET.ElementTree(root)
    return tree