from lxml import etree
from sec_parsers.style_detection import get_all_text
import warnings

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
        warnings.warn('DocumentType not found in metadata. Filing type set to 10K. If this is not correct, please set the filing type manually.')
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