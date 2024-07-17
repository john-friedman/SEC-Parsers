from sec_parsers.tag_detectors import LinkTagDetector, BoldTagDetector, StrongTagDetector, EmphasisTagDetector, ItalicTagDetector,\
      UnderlineTagDetector, TableTagDetector, ImageTagDetector, TableOfContentsTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector, BoldCSSDetector,UnderlineCSSDetector,ItalicCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup, SEC10KStringDetectorGroup,SEC8KStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text, get_elements_between_elements, get_text_between_elements,\
        set_background_color, remove_background_color, open_tree
from sec_parsers.style_detection import is_descendant_of_table
from sec_parsers.cleaning import clean_title
from sec_parsers.visualization_helper import headers_colors_list

from collections import deque
from lxml import etree

# need to remember to ignore hidden css in relative parsing
# TODO: refactor to reduce code duplication / annoying stuff like detectors all over the place
class HTMLParser:
    def __init__(self, **kwargs):
        self.element_detectors = [] # e.g. table image link etc
        self.add_element_detector(HiddenCSSDetector(recursive_rule='return', xml_rule='ignore'))
        self.add_element_detector(TableTagDetector(recursive_rule='return', xml_rule='text'))
        self.add_element_detector(ImageTagDetector(recursive_rule='return', xml_rule='ignore'))

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


    def detect_style_from_string(self,string,recursive_rule_list=[]):
        string_detectors = self.string_detector.string_detectors
        # subset
        if recursive_rule_list:
            string_detectors = [detector for detector in string_detectors if detector.recursive_rule in recursive_rule_list]
        
        for detector in string_detectors:
            result = detector.detect(string)
            if result != '':
                return (result,detector.recursive_rule)
        
        return ('','')
    


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
            string_style, recursive_rule = self.detect_style_from_string(text) 
            if string_style != '':
                parsing_string = string_style
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

            # logic for adding to element or parent element, may want to move later
            if element.tail is not None: # WIP think about this
                parent = element.getparent()
                parent_text = get_all_text(parent)

                # initialize parent parsing log
                parent.attrib['parsing_log'] = ''
                
                parent_string_style,parent_recursive_rule = self.detect_style_from_string(parent_text,recursive_rule_list=['return'])
                if parent_recursive_rule == 'return':
                    parent.attrib['parsing_string'] = parent_string_style
                    parent.attrib['parsing_log'] += f'recursive-{parent_string_style}'
                elif parent_recursive_rule == 'continue':
                    parent.attrib['parsing_string'] = parsing_string + parent_string_style
                    parent.attrib['parsing_log'] += f'recursive-{parsing_string + parent_string_style}'
                else:
                    pass
            else:
                element.attrib['parsing_string'] = parsing_string
                element.attrib['parsing_log'] += f'recursive-{parsing_string}'
        return
    
    
    def relative_parse(self,html):
        parsed_elements = deque(html.xpath('//*[@parsing_string]'))

        skip_strings = [] # Strings not to be processed by relative parsing
        for detector in self.element_detectors + self.string_detector.string_detectors:
            if detector.recursive_rule == 'return':
                skip_strings.append(detector.style)
        
        parsed_elements = deque([element for element in parsed_elements if element.get('parsing_string') not in skip_strings])

        while parsed_elements:
            parsed_element = parsed_elements.popleft()

            parsing_string = parsed_element.get('parsing_string')
            
            # WIP process bullet points

            # check if descendant of table, maybe move order
            if is_descendant_of_table(parsed_element):
                parent = parsed_element.xpath("./ancestor::table")[0]
                parent.attrib['parsing_string'] = parsing_string
                parsed_elements.appendleft(parent)

                # remove descendants parsing strings
                descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                for descendant in descendants_with_parsing_string:
                    descendant.attrib.pop('parsing_string')

                    if descendant in parsed_elements: # makes sure parsed_element is not removed twice
                        parsed_elements.remove(descendant)

                    descendant.attrib['parsing_log'] += f'relative-ancestor is table so removed parsing string;'
                
                continue

            # Checks if children have parsing strings
            # check that this is actacully used
            children = parsed_element.xpath("child::*")
            if children:
                descendants_with_parsing_string = parsed_element.xpath('.//*[@parsing_string]') # changed WIP
                if descendants_with_parsing_string:
                    parsed_element.attrib.pop('parsing_string')

                    parsed_element.attrib['parsing_log'] += f'relative-element parsing string removed due to children having parsing strings;'
                    continue

            if len(parsed_elements) == 0:
                next_element = None
            else:
                next_element = parsed_elements[0]
                
            elements_between = get_elements_between_elements(html, parsed_element, next_element)

            # Logic for e.g. item1 then new element BUSINESS bold emphasis to merge with item1
            if elements_between:
                parent = parsed_element.getparent()
                parent_text = get_all_text(parent)
                parent_string_style,parent_recursive_rule = self.detect_style_from_string(parent_text,recursive_rule_list=['return'])
                if parent_recursive_rule == 'return':
                    parent.attrib['parsing_string'] = parent_string_style
                    parent.attrib['parsing_log'] += f'relative-{parent_string_style} added due to elements between; '
                    

                    # remove descendants parsing strings
                    descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                    for descendant in descendants_with_parsing_string:
                        descendant.attrib.pop('parsing_string')
                        if descendant in parsed_elements: # makes sure parsed_element is not removed twice
                            parsed_elements.remove(descendant)
                        descendant.attrib['parsing_log'] += f'relative-removed parsing string due to elements between; '
                    
                    parsed_elements.appendleft(parent)

                elif parent_recursive_rule == 'continue':
                    parent.attrib['parsing_string'] = parsing_string + parent_string_style
                    parent.attrib['parsing_log'] += f'relative-{parsing_string + parent_string_style} added due to elements between; '

                    # remove descendants parsing strings
                    descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                    for descendant in descendants_with_parsing_string:
                        descendant.attrib.pop('parsing_string')

                        if descendant in parsed_elements: # makes sure parsed_element is not removed twice
                            parsed_elements.remove(descendant)

                        descendant.attrib['parsing_log'] += f'relative-removed parsing string due to elements between; '

                    parsed_elements.appendleft(parent)

                else:
                    pass

                

            if elements_between: # handles bold elements in paragraphs
                previous_element = parsed_element.getprevious()
                if previous_element is not None: 
                    text = get_text(previous_element).strip() # WIP: may introduce some issues
                    if previous_element.get('parsing_string') is None and text != '':
                        parsed_element.attrib.pop('parsing_string', None)
                        parsed_element.attrib['parsing_log'] += f'relative-removed parsing string due to previous element not having parsing string; '

    def clean_parse(self,html):
        """set ignore items etc"""
        parsed_elements = html.xpath('//*[@parsing_string]')

        ignore_strings = [item.style for item in self.all_detectors if item.xml_rule == 'ignore']
        print(ignore_strings)
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


    def construct_xml_tree(self,html):
        root = etree.Element('root')

        # add document node
        document_node = etree.Element('document', title = 'Document')
        root.append(document_node)
        
# WIP FIX numbers inside pagraphs sometimes parsing as page numbers
class SEC10KParser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)  # Call the parent's _init method

        self.insert_element_detector(TableOfContentsTagDetector(recursive_rule ='return',xml_rule ='text'),0)
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

        self.insert_element_detector(TableOfContentsTagDetector(recursive_rule ='return',xml_rule ='text'),0)
        self.string_detector = SEC8KStringDetectorGroup()

        self.color_dict.update({
                       'item;': '#B8860B',
                       'bullet point;': '#FAFAD2',
                       'table;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })