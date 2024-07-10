from lxml import etree
import re

from sec_parsers.style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text, is_paragraph,\
detect_hidden_element
from sec_parsers.xml_helper import get_text, set_background_color, remove_background_color, open_tree, element_has_text,get_text_between_elements,get_elements_between_elements
from sec_parsers.visualization_helper import headers_colors_dict, headers_colors_list
from sec_parsers.hierarchy import get_hierarchy, get_preceding_elements, find_last_index
from sec_parsers.cleaning import clean_title
#TODO add better attributes, and a bunch of other stuff

# html attributes, parsing_string, parsing_type
def recursive_parse(element):
    """ Recursively parse elements to detect potential headers """
    
    # if element is invisible, skip
    if detect_hidden_element(element):
        return

    if detect_table(element):
        if detect_table_of_contents(element) == "toc":
            element.attrib['parsing_string'] = 'table of contents;'
        else:
            element.attrib['parsing_string'] = 'table;'
        return
    elif detect_link(element):
        element.attrib['parsing_string'] = 'link;'
        return
    elif detect_image(element):
        element.attrib['parsing_string'] = 'image;'
        return

    text = get_text(element).strip()
    if text == '':
        for child in element.iterchildren():
            recursive_parse(child)
    else:
        string_style = detect_style_from_string(text)
        element_style = detect_style_from_element(element)
        parsing_string = string_style + element_style

        # check if text element, e.g. not header.  WIP
        if parsing_string == '':
            return


        # determines whether to add parsing string to element or parent
        if ((get_all_text(element) == '') and (element.tail is not None)):
            parent = element.getparent()
            parent.attrib['parsing_string'] = parsing_string + 'parent;'
        else:
            element.attrib['parsing_string'] = parsing_string

    return 

# WIP, may rearrange code blocks
# TODO add page number relative parsing, fix item parsing
def relative_parsing(html):
    """Looks at parsed html from recursive parsing and uses relative position to improve parsing."""
    # header rules
    # e.g. if has tail add to bold?
    parsed_elements = html.xpath('//*[@parsing_string]')
    for count, parsed_element in enumerate(parsed_elements):
        # e.g. find bullet point look for right neighbors, allow for any number of spaces
        parsing_string = parsed_element.get('parsing_string')
        if 'bullet point;' in parsing_string:
            if count < len(parsed_elements):
                next_element = parsed_elements[count+1]
                text_between = get_text_between_elements(html,parsed_element,next_element).strip()
                if text_between == '':
                    # delete attribute
                    next_element.attrib.pop('parsing_string')
                    # remove from parse_elements_list
                    parsed_elements.remove(next_element)
        # ignore these tags
        elif parsing_string in ['table of contents;','table;','link;','image;']:
            pass
        else:
            # check if two elements should be combined into one header
            if count < len(parsed_elements) - 1:
                # this is slow - could speed up function behind, or just subset to items for now
                if 'item;' in parsing_string:
                    next_element = parsed_elements[count+1]

                    elements_between = get_elements_between_elements(html,parsed_element,next_element)
                    if len(elements_between) == 0:
                        # I'm not sure how this will affect parsed_elements, so be careful
                        parent = parsed_element.getparent()
                        parent.attrib['parsing_string'] = parsing_string
                        parsed_elements.append(parent)

                        parsed_element.attrib.pop('parsing_string')
                        next_element.attrib.pop('parsing_string')

                        parsed_elements.remove(parsed_element)
                        parsed_elements.remove(next_element)
                else:
                    # handle emphasized elements in middle of paragraphs
                    previous_element = parsed_element.getprevious()
                    if previous_element is not None:
                        if previous_element.attrib.get('parsing_string') is not None:
                            pass
                        else:
                            parsed_element.attrib.pop('parsing_string')
                            parsed_elements.remove(parsed_element)


    return

def cleanup_parsing(html):
    # reads html and sets attributes
    parsed_elements = html.xpath('//*[@parsing_string]')
    for parsed_element in parsed_elements:
        parsing_string = parsed_element.get('parsing_string')
        parsing_type = parsing_string
        if 'part;' in parsing_string:
            parsing_type = 'part;'
        elif 'item;' in parsing_string:
            parsing_type = 'item;'
        elif 'signatures;' in parsing_string:
            parsing_type = 'signatures;'
        elif 'bullet point;' in parsing_string:
            parsing_type = None
        elif any([item in parsing_string for item in ['table of contents;','link;','image;','page number;']]):
            parsing_type = 'ignore;'
            
        if parsing_type is not None:
            # remove parent
            # WIP
            parsing_type = parsing_type.replace('parent;','')
            parsed_element.attrib['parsing_type'] = parsing_type


    #     elif ((parsing_string == 'item;') and (element.tail is not None)):
    #         parent = element.getparent()
    #         parent.attrib['parsing'] = parsing_string #+ 'parent;'

                # checks for items after risk factor which are text, but in italics
            # if ((parsing_string == 'italic-tag;') and (is_paragraph(text))):
            #     parsing_string = ''
            #     string_style = ''


    return html
        
def parse_10k(html):
    # recursive parse for style detection
    recursive_parse(html)

    # pruning based on relative locations
    relative_parsing(html)

    # standardizing certain elements such as part, item, signatures
    cleanup_parsing(html)

    return html

# 10q and 10k are the same for now
parse_10q = parse_10k

# TODO: make visualization easier to read at an instance by differentiating colors etc
def visualize(root):
    # remove style from all descendants so that background color can be set
    for descendant in root.iterdescendants():
        remove_background_color(descendant)

    # find all elements with parsing attribute
    elements = root.xpath('//*[@parsing_type]')
    # get all unique parsing values
    parsing_values = list(set([element.attrib['parsing_type'] for element in elements]))
    # create a color dict
    color_dict =dict(zip(parsing_values, headers_colors_list[:len(parsing_values)])) 
    # replace color dict values with values from headers_colors_dict
    for key in headers_colors_dict.keys():
        color_dict[key] = headers_colors_dict[key]
    for element in elements:
        # get attribute parsing
        parsing = element.attrib['parsing_type']
        if parsing == '':
            pass
        else:
            color = color_dict[parsing]
            set_background_color(element, color)

    open_tree(root)

# Heavily WIP
def construct_xml_tree(parsed_html):
    root = etree.Element('root')
    
    # find all parsing elements
    elements = parsed_html.xpath('//*[@parsing_type]')

    # find the first part parsing
    first_part_element = [element for element in elements if element.attrib['parsing_type'] == 'part;'][0]

    # find signature
    signature = [element for element in elements if 'signatures;' in element.attrib['parsing_type']][0]

    # subset elements between first part and signature
    elements = elements[elements.index(first_part_element):elements.index(signature)]

    # add the signature to the end of the elements. we are not processing the signature right now, just adding it to the end as an anchor
    elements.append(signature)

    element_parsing_types = [element.attrib['parsing_type'] for element in elements]

    # restrict certain headers
    restricted_headers = ['ignore;']
    # WIP
    element_parsing_types = [element_parsing_type for element_parsing_type in element_parsing_types if element_parsing_type not in restricted_headers]

    # get which headers are above which headers
    hierearchy = get_hierarchy(element_parsing_types)

    # start parsing
    node_list = []
    count = 0
    while count < len(elements)-1:
        element = elements[count]
        next_element = elements[count+1]

        # check if element is a restricted header, if so, add to text of previous node
        element_parsing_type = element.attrib['parsing_type']
        if element_parsing_type in restricted_headers:
            node_list[-1].text += get_text_between_elements(parsed_html,element, next_element)
            count += 1
            continue

        # construct node
        title = get_all_text(element)
        title = clean_title(title)
        text = get_text_between_elements(parsed_html,element, next_element)

        if element_parsing_type == 'part;':
            node_class = 'part'
        elif element_parsing_type == 'item;':
            node_class = 'item'
        elif element_parsing_type == 'signature;':
            node_class = 'signature'
        else:
            node_class = 'company_defined_section'

        node = etree.Element(node_class, title = title, parsing_type = element_parsing_type)
        node.text = text

        # should return a list of headers that are above the current header
        rulers = get_preceding_elements(hierearchy, element_parsing_type)

        # get the parsing strings of the nodes in the node_list
        node_parsing_types= [node.attrib['parsing_type'] for node in node_list]

        # find the last element in the node_parsing_strings which is in rulers
        index = find_last_index(node_parsing_types, rulers)
        if element_parsing_type == 'part;':
            root.append(node)
            node_list = [node]
        elif len(node_list) == 0:
            # add node to root 
            root.append(node)
            # add node to node_list
            node_list = [node]
        elif index == -1:
            # add node to last node in node_list
            node_list[-1].append(node)
            # add node to node_list
            node_list.append(node)
        else:
            # subset node_list to index
            node_list = node_list[:index+1]
            # add node to last node in node_list
            node_list[-1].append(node)
            # add node to node_list
            node_list.append(node)

        count += 1

    return root

def detect_filing_type(html):
    """TODO"""
    return "10K"

# Think about inheritance
class Parser:
    def __init__(self, html):
        self._setup_html(html)
        self.parsed_html = None
        self.hierarchy = None # need to implement
        self.xml = None
        self.filing_type = None

    def _setup_html(self,html):
        parser = etree.HTMLParser(encoding='utf-8',remove_comments=True)
        parsed_html = etree.fromstring(html, parser)
        self.html = parsed_html

    # make util
    def _detect_filing_type(self):
        filing_type = detect_filing_type(self.html)
        self.filing_type = filing_type

    def _parse_10k(self):
        self.parsed_html = parse_10k(self.html)

    def _parse_10q(self):
        self.parsed_html = parse_10q(self.html)

    def set_filing_type(self, filing_type):
        self.filing_type = filing_type

    def parse(self):
        if self.filing_type is None:
            self._detect_filing_type()

        if self.filing_type == '10K':
            self._parse_10k()
        elif self.filing_type == '10Q':
            self._parse_10q()
        else:
            raise ValueError('Filing type not detected')

    def visualize(self):
        visualize(self.html)

    def to_xml(self):
        self.xml = construct_xml_tree(self.parsed_html)

    # functions to interact with xml

    # Find #
    def find_nodes_by_title(self,title):
        if self.xml is None:
            self.to_xml()

        return self.xml.xpath(f"//*[@title='{title}']")
    
    def find_nodes_by_desc(self,desc):
        if self.xml is None:
            self.to_xml()
        return self.xml.xpath(f"//*[@desc='{desc}']")
    
    def find_nodes_by_text(self, text):
        """Find a node by text."""

        if self.xml is None:
            self.to_xml()

        return self.xml.xpath(f"//*[contains(text(), '{text}')]")
    
    def fuzzy_find_nodes_by_title(self,title):
        # TODO: implement
        pass
    # Interact with Node #

    # Note, needs refactor, also needs better spacing fix with text.
    def get_node_text(self,node):
        """Gets all text from a node, including desc string."""
        text = ''
        text += node.attrib.get('title','') + '\n'

        node_text = node.text
        if node_text is not None:
            text += node.text + '\n'
            
        for child in node:
            text += self.get_node_text(child)
        
        return text
    
    # Interact with tree #

    # TODO: better names
    def get_node_tree(self,node=None, level=0):
        if node is None:
            node = self.xml
        tree_string = node.tag
        for child in node:
            tree_string += '\n' + '|-' * level + self.get_node_tree(child, level + 1)
        return tree_string
    
    def get_node_tree_attributes(self,node=None,level=0,attribute='title'):
        if node is None:
            node = self.xml
            
        tree_atrib = node.attrib.get(attribute,'')
        for child in node:
            tree_atrib += '\n' + '|-' * level + self.get_node_tree_attributes(child, level + 1,attribute)

        return tree_atrib
    
    # Save to file #
    def save_xml(self, filename):
        if self.xml is None:
            self.to_xml()

        with open(filename, 'wb') as f:
            f.write(etree.tostring(self.xml))

    # TODO: Implement
    def save_csv(self, filename):
        pass

    # TODO: implement
    def save_dta(self, filename):
        pass

        
