from sec_parsers.string_detector_groups import HeaderStringDetectorGroup, SEC10KStringDetectorGroup,SEC8KStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text, get_elements_between_elements, get_text_between_elements,\
        set_background_color, remove_background_color, open_tree
from sec_parsers.style_detection import is_descendant_of_table
from sec_parsers.cleaning import clean_title, is_string_in_middle
from sec_parsers.visualization_helper import headers_colors_list
from sec_parsers.hierachy import assign_header_levels
from collections import deque
from lxml import etree

from sec_parsers.element_detector_groups import HeaderElementDetectorGroup, SEC10KElementGroup, SEC8KElementGroup

# need to remember to ignore hidden css in relative parsing
# TODO: refactor to reduce code duplication / annoying stuff like detectors all over the place

# TODO, probably add autosort later
class HTMLParser:
    def __init__(self, **kwargs):
        self.element_detector_group = HeaderElementDetectorGroup() # parses elements
        self.string_detector_group = HeaderStringDetectorGroup() # parses strings
        self.color_dict = {'ignore;': '#f2f2f2'} # If you want certain parsing types to have certain colors

        self._init(**kwargs)
        self.all_detectors = self.element_detector_group.element_detectors + self.string_detector_group.string_detectors

    def _init(self, **kwargs):
        # This method is meant to be overridden by subclasses
        pass


    def detect_style_from_string(self,string,rule_list=[]):
        string_detectors = self.string_detector_group.string_detectors
        # subset
        if rule_list: # WIP
            string_detectors = [detector for detector in string_detectors if detector.parsing_rule in rule_list]
        
        result = ''
        for detector in string_detectors:
            string_style = detector.detect(string)
            if string_style != '':
                parsing_rule = detector.parsing_rule
                if parsing_rule == 'return':
                    return string_style, parsing_rule
                else:
                    result += string_style
        
        return (result,'continue')
    
    
    def detect_style_from_element(self,element,rule_list=[]):
        element_detectors = self.element_detector_group.element_detectors
        # subset
        if rule_list: # WIP
            element_detectors = [detector for detector in element_detectors if detector.parsing_rule in rule_list]
        
        result = ''
        for detector in element_detectors:
            element_style = detector.detect(element)
            if element_style != '':
                parsing_rule = detector.parsing_rule
                if parsing_rule == 'return':
                    return element_style, parsing_rule
                else:
                    result += element_style
        
        return (result,'continue')
    

    # i think we can modify this to make relative parser mostly useless.
    def recursive_parse(self, element):
        # initialize parsing log
        element.attrib['parsing_log'] = ''
        parsing_string = ''

        # detect style from elements
        result, parsing_rule = self.detect_style_from_element(element)
        if parsing_rule == 'return':
            parsing_string = result
            element.attrib['parsing_string'] = parsing_string
            element.attrib['parsing_log'] += f'recursive-{parsing_string}'
            return
        else:
            parsing_string += result
            element.attrib['parsing_log'] += f'recursive-{result}'


        string = get_text(element).strip()
        if string == '':# recursion
            for child in element.iterchildren():
                self.recursive_parse(child)
        else:
            # detect style from strings
            result, parsing_rule = self.detect_style_from_string(string)
            if parsing_rule == 'return':
                parsing_string = result
                element.attrib['parsing_string'] = parsing_string
                element.attrib['parsing_log'] += f'recursive-{parsing_string}'
                return
            else:
                parsing_string += result
                element.attrib['parsing_log'] += f'recursive-{result}'

            element.attrib['parsing_string'] = parsing_string
                
        return
    
    # I think this is fine for now
    def relative_parse(self,html):
        parsed_elements = deque(html.xpath('//*[@parsing_string]'))


        while parsed_elements:
            parsed_element = parsed_elements.popleft()
            parsing_string = parsed_element.get('parsing_string')
            element_text = get_text(parsed_element).strip()

            # WIP - gets ancestor whose text is not equal to element text
            flag = True
            while flag:
                parent = parsed_element.getparent()
                parent_text = get_all_text(parent).strip()
                if parent_text != element_text:
                    flag = False
                flag = False

            
            #WIP
            # code to merge elements - e.g. item 1 and business
            parent_string_style, _ = self.detect_style_from_string(parent_text,rule_list=['return']) 
            if parent_string_style != '':
                parent.attrib['parsing_string'] = parent_string_style
                parent.attrib['parsing_log'] += f'relative-merged with parent;'

                # remove descendants parsing string
                for descendant in parent.iterdescendants():
                    descendant.attrib.pop('parsing_string', None)
                    descendant.attrib['parsing_log'] += 'relative-removed as merged with parent;'
                    # remove from queue
                    if descendant in parsed_elements:
                        parsed_elements.remove(descendant)

                continue
            

            # remove parsing string if in the middle of text - I like this
            if is_string_in_middle(parent_text, element_text):
                parsed_element.attrib.pop('parsing_string')
                parsed_element.attrib['parsing_log'] += f'relative-popped as it was in middle;'
                continue


    # Works
    def clean_parse(self,html):
        """set ignore items etc"""
        parsed_elements = html.xpath('//*[@parsing_string]')

        # figure out how to manage remove, skip, and header strigns here
        remove_strings = [item.style for item in self.all_detectors if item.cleaning_rule == 'remove']
        skip_strings = [item for item in self.all_detectors if item.cleaning_rule == 'skip']
        for parsed_element in parsed_elements:
            parsing_string = parsed_element.get('parsing_string')   
            # check if ignore
            if parsing_string in remove_strings:
                parsed_element.attrib['parsing_type'] = 'ignore;'
                parsed_element.attrib['parsing_log'] += 'clean-parse-ignored;'
            # check if text
            elif parsing_string in skip_strings:
                parsed_element.attrib['parsing_log'] += 'clean-parse-text;'
            else:
                parsed_element.attrib['parsing_type'] = parsing_string
                parsed_element.attrib['parsing_log'] += 'clean-parse-header;'


    # works
    def visualize(self,html):
        # remove style from all descendants so that background color can be set
        for descendant in html.iterdescendants():
            remove_background_color(descendant)

        # find all elements with parsing attribute
        elements = html.xpath('//*[@parsing_type]')
        # get all unique parsing values
        parsing_values = list(set([element.attrib['parsing_type'] for element in elements]))
        color_dict =dict(zip(parsing_values, headers_colors_list[:len(parsing_values)]))
        color_dict.update(self.color_dict)
        # we want header scale, ignore color

        for element in elements:
            # get attribute parsing
            parsing = element.attrib['parsing_type']
            if parsing == '':
                pass
            else:
                color = color_dict[parsing]
                set_background_color(element, color)

        open_tree(html)

    # WIP
    def construct_xml_tree(self, html):
        root = etree.Element('root')
        document_node = etree.Element('document', title='Document')
        root.append(document_node)

        parsed_elements = html.xpath('//*[@parsing_type]')

        # WIP
        parsed_elements = [element for element in parsed_elements if element.get('parsing_type') != 'ignore;']

        # Handle introduction (elements before first 0 level header)
        base_headers = ['part;', 'item;,' 'signatures;'] # FIX
        first_header = [item for item in parsed_elements if item.attrib['parsing_type'] in base_headers][0]

        first_index = parsed_elements.index(first_header)
        introduction_node = etree.Element('introduction', title='Introduction')
        introduction_node.text = get_text_between_elements(html,start_element=None, end_element=parsed_elements[first_index])
        document_node.append(introduction_node)

        # subset by first_index
        parsed_elements = parsed_elements[first_index:]
        parsed_types = [element.attrib['parsing_type'] for element in parsed_elements]

        hierarchy_dict = {'part;': 0, 'item;': 1,'signatures;': 0}
        levels = assign_header_levels(parsed_types,hierarchy_dict=hierarchy_dict)

        # Parse hierarchical structure
        stack = [(- 1, document_node)]  # (level, node) pairs

        for i, (level, parsed_element) in enumerate(zip(levels, parsed_elements), start=0):
            node = etree.Element('header', title=clean_title(get_all_text(parsed_element)))

            # Get the next element (if any)
            next_element = parsed_elements[i + 1] if i + 1 < len(parsed_elements) else None

            # Extract text between current element and next element
            node.text = get_text_between_elements(html,start_element=parsed_element, end_element=next_element)

            # Find the appropriate parent node
            while stack and level <= stack[-1][0]: # WIP
                stack.pop()

            # Append to the appropriate parent
            stack[-1][1].append(node)
            stack.append((level, node))

        return root

        
# WIP FIX numbers inside pagraphs sometimes parsing as page numbers
class SEC10KParser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)  # Call the parent's _init method

        self.element_detector_group = SEC10KElementGroup()
        self.string_detector_group = SEC10KStringDetectorGroup()

        self.color_dict.update({'part;': '#B8860B',
                       'item;': '#BDB76B',
                       'bullet point;': '#FAFAD2',
                       'table;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })


# 10Q and 10K are the same for now
class SEC10QParser(SEC10KParser):
    pass

class SEC8KParser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)

        self.element_detector_group = SEC8KElementGroup()
        self.string_detector_group = SEC8KStringDetectorGroup()
        self.color_dict.update({
                       'item;': '#B8860B',
                       'bullet point;': '#FAFAD2',
                       'table;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })