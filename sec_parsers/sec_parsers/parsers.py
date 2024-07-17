from lxml import etree
import re
import csv
from collections import deque

from sec_parsers.style_detection import detect_style_from_string, detect_style_from_element, detect_table, detect_image,detect_table_of_contents, get_all_text, is_paragraph,\
detect_hidden_element, is_descendant_of_table
from sec_parsers.xml_helper import get_text, set_background_color, remove_background_color, open_tree,get_text_between_elements,get_elements_between_elements
from sec_parsers.visualization_helper import headers_colors_dict, headers_colors_list
from sec_parsers.cleaning import clean_title, part_pattern
#TODO add better attributes, and a bunch of other stuff

        

# WIP: convert special checked boxes into True / False, etc
def parse_metadata(html):
    """WIP"""
    metadata_dict = {}
    # select all elements with attribute name and first part of attribute is 'dei'
    elements = html.xpath('//*[@name]')
    elements = [element for element in elements if element.attrib['name'].lower().startswith('dei')]
    for element in elements:
        name = element.attrib['name']
        name = name.replace('dei:','')
        metadata_dict[name] = get_all_text(element)
    return metadata_dict

def detect_filing_type(metadata):
    """WIP"""
    if 'DocumentType' in metadata.keys():
        return metadata['DocumentType']
    else:
        print('DocumentType not found in metadata. Filing type set to 10K. If this is not correct, please set the filing type manually.')
        return '10-K'

def setup_html(html):
        # Find the start of the HTML content. This is necessary because the HTML content is not always at the beginning of the file.
        body_start = html.find('<BODY')
        if body_start == -1:
            body_start = html.find('<body')

        if body_start != -1:
            html = html[body_start:]

        parser = etree.HTMLParser(encoding='utf-8',remove_comments=True)
        html = etree.fromstring(html, parser)

        return html