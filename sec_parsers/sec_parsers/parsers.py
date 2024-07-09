from lxml import etree
import re

from sec_parsers.style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text, is_paragraph
from sec_parsers.xml_helper import get_text, set_background_color, remove_background_color, open_tree, element_has_text,get_text_between_elements,get_elements_between_elements
from sec_parsers.visualization_helper import headers_colors_dict, headers_colors_list
from sec_parsers.hierarchy import get_hierarchy, get_preceding_elements, find_last_index


#TODO add better attributes, and a bunch of other stuff

# The function for conversion to xml is the most recent and most WIP, will rewrite substantially.

# Needs general code cleanup
# removed parent for now, need to setup better attributes for error detection and parsing
def recursive_parse(element):
    # check if visible
    style = element.attrib.get('style')
    if style is not None:
        if 'display:none' in re.sub(' ','',style):
            return

    if element.attrib.get('parsing') == None:
        element.attrib['parsing'] = ''

    values = element.values()
    if len(values) == 1:
        if 'display:none' in values[0]:
            return

    if detect_table(element):
        if detect_table_of_contents(element) == "toc":
            element.attrib['parsing'] = 'table of contents;'
        else:
            element.attrib['parsing'] = 'table;'
        return

    if detect_link(element):
        element.attrib['parsing'] = 'link;'
        return
    
    if detect_image(element):
        element.attrib['parsing'] = 'image;'
        return

    text = get_text(element).strip()
    if text == '':
        for child in element.iterchildren():
            recursive_parse(child)
    else:
        string_style = detect_style_from_string(text)
        element_style = detect_style_from_element(element)

        parsing_string = ''

        # if no style found / pruning / cleaning
        if (string_style+element_style == ''):
            element.attrib['parsing'] = ''
        else:

            if any(style in element_style for style in ['font-weight:bold','font-weight:700;','b-tag;','strong-tag;']):
                parsing_string += 'bold-tag;'

            if any(style in element_style for style in ['font-style:italic','em','i']):
                parsing_string += 'italic-tag;'

            if any(style in element_style for style in ['text-decoration:underline','u']):
                parsing_string += 'underline-tag;'

            # check for items after risk factor which are text, but in italics
            if ((parsing_string == 'italic-tag;') and (is_paragraph(text))):
                parsing_string = ''
                string_style = ''

            # change this to functions
            if string_style == 'item;':
                parsing_string = 'item;'
                string_style = ''
            elif string_style == 'part;':
                parsing_string = 'part;'
                string_style = ''
            elif string_style == 'signatures':
                parsing_string = 'signature;'
                string_style = ''

            # relative parsing - change parsing based on previous element
            previous_element = element.getprevious()
            if previous_element is not None:
                if element_has_text(previous_element):
                    # change to go back further if empty?
                    previous_element_parsing_string = previous_element.attrib.get('parsing')
                    if previous_element_parsing_string == 'bullet point;':
                        string_style = ''
                        parsing_string = ''
                    elif previous_element_parsing_string == '':
                        string_style = ''
                        parsing_string = ''
                    elif previous_element_parsing_string == 'item;':
                        string_style = 'item;'
                        parsing_string = ''
                    elif previous_element_parsing_string == 'part;':
                        string_style = 'part;'
                        parsing_string = ''


            parsing_string += string_style

            if ((get_all_text(element) == '') and (element.tail is not None)):
                parent = element.getparent()
                parent.attrib['parsing'] = parsing_string #+ 'parent;'
            elif ((parsing_string == 'item;') and (element.tail is not None)):
                parent = element.getparent()
                parent.attrib['parsing'] = parsing_string #+ 'parent;'
            else:
                element.attrib['parsing'] = parsing_string

    return 
        
def parse_10k(html):
    parser = etree.HTMLParser(encoding='utf-8',remove_comments=True)
    parsed_html = etree.fromstring(html, parser)
    recursive_parse(parsed_html)
    return parsed_html

# 10q and 10k are the same for now
parse_10q = parse_10k

# need to add static colors at some point
# palette for headings
# palette for identified stuff
def visualize(root):
    # remove style from all descendants so that background color can be set
    for descendant in root.iterdescendants():
        remove_background_color(descendant)

    # find all elements with parsing attribute
    elements = root.xpath('//*[@parsing]')
    # get all unique parsing values
    parsing_values = list(set([element.attrib['parsing'] for element in elements]))
    # create a color dict
    color_dict =dict(zip(parsing_values, headers_colors_list[:len(parsing_values)])) 
    # replace color dict values with values from headers_colors_dict
    for key in headers_colors_dict.keys():
        color_dict[key] = headers_colors_dict[key]
    for element in elements:
        # get attribute parsing
        parsing = element.attrib['parsing']
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
    elements = parsed_html.xpath('//*[@parsing]')
    # subset by elements where parsing is not empty
    elements = [element for element in elements if element.attrib['parsing'] != '']
    # find the first part parsing
    first_part_element = [element for element in elements if element.attrib['parsing'] == 'part;'][0]
    # find signature
    signature = [element for element in elements if 'signatures;' in element.attrib['parsing']][0]

    # subset elements between first part and signature
    elements = elements[elements.index(first_part_element):elements.index(signature)]
    # add the signature to the end of the elements. we are not processing the signature right now, just adding it to the end as an anchor
    elements.append(signature)

    element_parsing_strings = [element.attrib['parsing'] for element in elements]

    # restrict certain headers
    restricted_headers = ['table;','table of contents;','image;','link;','bullet point;','page number;']
    element_parsing_strings = [element_parsing_string for element_parsing_string in element_parsing_strings if element_parsing_string not in restricted_headers]
    # remove parent from parsing strings
    element_parsing_strings = [re.sub('parent;','',element_parsing_string) for element_parsing_string in element_parsing_strings]

    # get which headers are above which headers
    hierearchy = get_hierarchy(element_parsing_strings)

    # start parsing
    node_list = []
    count = 0
    while count < len(elements)-1:
        element = elements[count]
        next_element = elements[count+1]

        # check if element is a restricted header, if so, add to text of previous node
        element_parsing_string = element.attrib['parsing']
        if element_parsing_string in restricted_headers:
            node_list[-1].text += get_text_between_elements(parsed_html,element, next_element)
            count += 1
            continue

        # construct node
        desc = get_all_text(element)
        title = re.sub(' ','',desc.strip().lower())
        text = get_text_between_elements(parsed_html,element, next_element)

        if element_parsing_string == 'part;':
            node_class = 'part'
        elif element_parsing_string == 'item;':
            node_class = 'item'
        else:
            node_class = 'section'

        node = etree.Element(node_class, title = title, desc= desc, parsing = element_parsing_string)
        node.text = text

        # should return a list of headers that are above the current header
        rulers = get_preceding_elements(hierearchy, element_parsing_string)

        # get the parsing strings of the nodes in the node_list
        node_parsing_strings = [node.attrib['parsing'] for node in node_list]

        # find the last element in the node_parsing_strings which is in rulers
        index = find_last_index(node_parsing_strings, rulers)
        if element_parsing_string == 'part;':
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
    pass


# Think about inheritance
class Parser:
    def __init__(self, html):
        self.html = html
        self.parsed_html = None
        self.hierarchy = None # need to implement
        self.xml = None
        self.filing_type = None

    # make util
    def _detect_filing_type(self):
        # detect filing type from html
        filing_type = "10K" #detect_filing_type(self.html)
        self.filing_type = filing_type

    def _parse_10k(self):
        self.parsed_html = parse_10k(self.html)

    def _parse_10q(self):
        self.parsed_html = parse_10q(self.html)


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
        if self.parsed_html is None:
            self.parse_10k()
        visualize(self.parsed_html)

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
    # Interact with Node #

    # Note, needs refactor, also needs better spacing fix with text.
    def get_node_text(self,node):
        """Gets all text from a node, including desc string."""
        text = ''
        text += node.attrib.get('desc','') + '\n'

        node_text = node.text
        if node_text is not None:
            text += node.text + '\n'
            
        for child in node:
            text += self.get_node_text(child)
        
        return text
    
    # Interact with tree #

    # TODO: better names
    def get_node_tree(self,node, level=0):
        tree_string = node.tag
        for child in node:
            tree_string += '\n' + '|-' * level + self.get_node_tree(child, level + 1)
        return tree_string
    
    def get_node_tree_attributes(self,node,level=0,attribute='title'):
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

        
