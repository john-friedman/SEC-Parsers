from sec_parsers.tag_detectors import LinkTagDetector, BoldTagDetector, StrongTagDetector, EmphasisTagDetector, ItalicTagDetector,\
      UnderlineTagDetector, TableTagDetector, ImageTagDetector, TableOfContentsTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector, BoldCSSDetector,UnderlineCSSDetector,ItalicCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup, SEC10KStringDetectorGroup,SEC8KStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text, get_elements_between_elements, get_text_between_elements,\
        set_background_color, remove_background_color, open_tree
from sec_parsers.style_detection import is_descendant_of_table
from sec_parsers.cleaning import clean_title, is_string_in_middle
from sec_parsers.visualization_helper import headers_colors_list
from sec_parsers.hierachy import assign_header_levels
from collections import deque
from lxml import etree

# need to remember to ignore hidden css in relative parsing
# TODO: refactor to reduce code duplication / annoying stuff like detectors all over the place
class HTMLParser:
    def __init__(self, **kwargs):
        self.element_detectors = [] # e.g. table image link etc
        self.add_element_detector(HiddenCSSDetector(recursive_rule='return', xml_rule='ignore',relative_rule='ignore'))
        self.add_element_detector(TableTagDetector(recursive_rule='return', xml_rule='text',relative_rule='ignore'))
        self.add_element_detector(ImageTagDetector(recursive_rule='return', xml_rule='ignore',relative_rule='ignore'))

        self.string_detector = HeaderStringDetectorGroup() # strings that should be detected

        self.tag_detectors = [LinkTagDetector(),BoldTagDetector(),StrongTagDetector(),EmphasisTagDetector(),ItalicTagDetector(),UnderlineTagDetector()]
        self.css_detectors = [BoldCSSDetector(),UnderlineCSSDetector(),ItalicCSSDetector()]
        self.style_detectors = self.css_detectors + self.tag_detectors # e.g. strong, emphasis, italic, underline, etc

        self.color_dict = {'ignore;': '#f2f2f2'} # If you want certain parsing types to have certain colors

        self._init(**kwargs)
        self.update_all_detectors()

    def _init(self, **kwargs):
        # This method is meant to be overridden by subclasses
        pass


    def update_all_detectors(self):
        self.all_detectors = self.element_detectors + self.style_detectors + self.string_detector.string_detectors
    def insert_element_detector(self, element_detector,index):
        self.element_detectors.insert(index,element_detector)

    def insert_element_detectors(self, element_detectors):
        self.element_detectors = element_detectors + self.element_detectors

    def add_element_detector(self, element_detector):
        self.element_detectors.append(element_detector)

    def remove_element_detector(self, element_detector):
        self.element_detectors.remove(element_detector)


    def detect_style_from_string(self,string,attribute,rule_list=[]):
        string_detectors = self.string_detector.string_detectors
        # subset
        if rule_list:
            string_detectors = [detector for detector in string_detectors if getattr(detector, attribute) in rule_list]
        
        for detector in string_detectors:
            result = detector.detect(string)
            if result != '':
                return (result,getattr(detector, 'recursive_rule'))
        
        return ('','')
    

    # i think we can modify this to make relative parser mostly useless.
    def recursive_parse(self, element):
        # initialize parsing log
        element.attrib['parsing_log'] = ''
        # think about return rules here
        for detector in self.element_detectors:
            result = detector.detect(element)
            if result != '':
                element.attrib['parsing_string'] = result
                element.attrib['parsing_log'] += f'recursive-{result}'
                return
            
        text = get_text(element).strip()
        if text == '':
            for child in element.iterchildren():
                self.recursive_parse(child)
        else:
            parsing_string = ''
            string_style, recursive_rule = self.detect_style_from_string(text,attribute='recursive_rule') 
            if string_style != '':
                parsing_string = string_style
                if recursive_rule == 'return':
                    element.attrib['parsing_string'] = parsing_string
                    element.attrib['parsing_log'] += f'recursive- 2nd run detect {parsing_string}'
                    return
            else:
                recursive_rule = 'continue'

            if recursive_rule=='continue':
                # other should continue to style detectors
                for detector in self.style_detectors:
                    result = detector.detect(element)
                    if result != '':
                        parsing_string += detector.style

                # check parsing string is not empty
                if parsing_string == '':
                    return

                element.attrib['parsing_string'] = parsing_string
                element.attrib['parsing_log'] += f'recursive-{parsing_string}'
        return
    
    def relative_parse(self,html):
        parsed_elements = deque(html.xpath('//*[@parsing_string]'))


        while parsed_elements:
            parsed_element = parsed_elements.popleft()
            parsing_string = parsed_element.get('parsing_string')
            element_text = get_text(parsed_element).strip()

            # get ancestor whose text is not the same after trimming #WIP
            flag = True
            while flag:
                parent = parsed_element.getparent()
                parent_text = get_all_text(parent).strip()
                if parent_text != element_text:
                    flag = False
                flag = False

            
            #WIP
            # code to merge elements
        

            # remove parsing string if in the middle of text - I like this
            if is_string_in_middle(parent_text, element_text):
                parsed_element.attrib.pop('parsing_string')
                parsed_element.attrib['parsing_log'] += f'relative-popped as it was in middle;'
                continue


    
    def clean_parse(self,html):
        """set ignore items etc"""
        parsed_elements = html.xpath('//*[@parsing_string]')

        ignore_strings = [item.style for item in self.all_detectors if item.xml_rule == 'ignore']
        text_strings = [item for item in self.element_detectors if item.xml_rule == 'text']
        for parsed_element in parsed_elements:

            parsing_string = parsed_element.get('parsing_string')   
            # check if ignore
            if parsing_string in ignore_strings:
                parsed_element.attrib['parsing_type'] = 'ignore;'
                parsed_element.attrib['parsing_log'] += 'clean-parse-ignored;'
                
            # check if text
            elif parsing_string in text_strings:
                parsed_element.attrib['parsing_log'] += 'clean-parse-text;'
            else:
                parsed_element.attrib['parsing_type'] = parsing_string
                parsed_element.attrib['parsing_log'] += 'clean-parse-header;'

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


    def construct_xml_tree(self, html):
        root = etree.Element('root')
        document_node = etree.Element('document', title='Document')
        root.append(document_node)

        parsed_elements = html.xpath('//*[@parsing_type]')
        parsed_types = [element.attrib['parsing_type'] for element in parsed_elements]
        hierarchy_dict = {'part;': 0, 'item;': 1,'signatures;': 0}
        levels = assign_header_levels(parsed_types,hierarchy_dict=hierarchy_dict)

        # Handle introduction (elements before first 0 level header)
        first_index = next((i for i, level in enumerate(levels) if level == 0), len(levels))
        introduction_node = etree.Element('introduction', title='Introduction')
        introduction_node.text = get_text_between_elements(html,start_element=None, end_element=parsed_elements[first_index])
        document_node.append(introduction_node)

        # Parse hierarchical structure
        stack = [(- 1, document_node)]  # (level, node) pairs

        for i, (level, parsed_element) in enumerate(zip(levels[first_index:], parsed_elements[first_index:]), start=first_index):
            node = etree.Element('header', title=parsed_element.get('parsing_type'))
            
            # Get the next element (if any)
            next_element = parsed_elements[i + 1] if i + 1 < len(parsed_elements) else None
            
            # Extract text between current element and next element
            node.text = get_text_between_elements(html,start_element=parsed_element, end_element=next_element)

            # Find the appropriate parent node
            while stack and level <= stack[-1][0]:
                stack.pop()

            # Append to the appropriate parent
            stack[-1][1].append(node)
            stack.append((level, node))

        return root

        
# WIP FIX numbers inside pagraphs sometimes parsing as page numbers
class SEC10KParser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)  # Call the parent's _init method

        self.insert_element_detector(TableOfContentsTagDetector(recursive_rule ='return',xml_rule ='text',relative_rule='ignore'),0)
        self.string_detector = SEC10KStringDetectorGroup()

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

        self.insert_element_detector(TableOfContentsTagDetector(recursive_rule ='return',xml_rule ='text',relative_rule='ignore'),0)
        self.string_detector = SEC8KStringDetectorGroup()

        self.color_dict.update({
                       'item;': '#B8860B',
                       'bullet point;': '#FAFAD2',
                       'table;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })