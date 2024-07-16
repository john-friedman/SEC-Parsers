from sec_parsers.tag_detectors import LinkTagDetector, BoldTagDetector, StrongTagDetector, EmphasisTagDetector, ItalicTagDetector,\
      UnderlineTagDetector, TableTagDetector, ImageTagDetector, TableOfContentsTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector, BoldCSSDetector,UnderlineCSSDetector,ItalicCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup, SEC10KStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text, get_elements_between_elements
from sec_parsers.style_detection import is_descendant_of_table
from collections import deque

# need to remember to ignore hidden css in relative parsing

class HTMLParser:
    def __init__(self):
        self.element_detectors = [] # e.g. table image link etc
        self.add_element_detector(HiddenCSSDetector(recursive_rule='return', relative_rule='skip'))
        self.add_element_detector(TableTagDetector(recursive_rule='return', relative_rule='skip'))
        self.add_element_detector(ImageTagDetector(recursive_rule='return',relative_rule='skip'))

        self.string_detector = HeaderStringDetectorGroup() # strings that should be detected

        self.tag_detectors = [LinkTagDetector(),BoldTagDetector(),StrongTagDetector(),EmphasisTagDetector(),ItalicTagDetector(),UnderlineTagDetector()]
        self.css_detectors = [HiddenCSSDetector(),BoldCSSDetector(),UnderlineCSSDetector(),ItalicCSSDetector()]
        self.style_detectors = self.css_detectors + self.tag_detectors # e.g. strong, emphasis, italic, underline, etc


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
        # think about return rules here
        for detector in self.element_detectors:
            result = detector.detect(element)
            if result != '':
                element.attrib['parsing_string'] = result
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
                parent_string_style,parent_recursive_rule = self.detect_style_from_string(parent_text,recursive_rule_list=['return'])
                if parent_recursive_rule == 'return':
                    parent.attrib['parsing_string'] = parent_string_style
                elif parent_recursive_rule == 'continue':
                    parent.attrib['parsing_string'] = parsing_string + parent_string_style
                else:
                    pass
            else:
                element.attrib['parsing_string'] = parsing_string
        return
    
    
    def relative_parse(self,html):
        parsed_elements = deque(html.xpath('//*[@parsing_string]'))

        skip_strings = [] # Strings not to be processed by relative parsing
        for detector in self.element_detectors + self.string_detector.string_detectors:
            if detector.recursive_rule == 'return':
                skip_strings.append(detector.style)
        
        parsed_elements = deque([element for element in parsed_elements if element.get('parsing_string') not in skip_strings])
        print(skip_strings)

        while parsed_elements:
            parsed_element = parsed_elements.popleft()
            parsing_string = parsed_element.get('parsing_string')

            # Checks if children have parsing strings
            # check that this is actacully used
            children = parsed_element.xpath("child::*")
            if children:
                descendants_with_parsing_string = parsed_element.xpath('.//*[@parsing_string]') # changed WIP
                if descendants_with_parsing_string:
                    parsed_element.attrib.pop('parsing_string')
                    parsed_elements.remove(parsed_element)
                    continue
            
            # WIP process bullet points

            # check if descendant of table
            if is_descendant_of_table(parsed_element):
                parent = parsed_element.xpath("./ancestor::table")[0]
                parent.attrib['parsing_string'] = parsing_string
                parsed_elements.appendleft(parent)

                # remove descendants parsing strings
                descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                for descendant in descendants_with_parsing_string:
                    descendant.attrib.pop('parsing_string')
                    parsed_elements.remove(descendant)
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

                        # remove descendants parsing strings
                        descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                        for descendant in descendants_with_parsing_string:
                            descendant.attrib.pop('parsing_string')
                            parsed_elements.remove(descendant)

                    elif parent_recursive_rule == 'continue':
                        parent.attrib['parsing_string'] = parsing_string + parent_string_style

                        # remove descendants parsing strings
                        descendants_with_parsing_string = parent.xpath('.//*[@parsing_string]')
                        for descendant in descendants_with_parsing_string:
                            descendant.attrib.pop('parsing_string')
                            parsed_elements.remove(descendant)
                    else:
                        pass

                    parsed_elements.appendleft(parent)

                if elements_between: # handles bold elements in paragraphs
                    previous_element = parsed_element.getprevious()
                    if previous_element is not None: 
                        text = get_text(previous_element).strip() # WIP: may introduce some issues
                        if previous_element.get('parsing_string') is None and text != '':
                            parsed_element.attrib.pop('parsing_string', None)
                            parsed_elements.remove(parsed_element)

                

        


class SEC10KParser(HTMLParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.insert_element_detector(TableOfContentsTagDetector(recursive_rule ='return',
                                                                 relative_rule='skip'),0) # change to right before table detector 
        self.string_detector = SEC10KStringDetectorGroup() #WIP

 
class SEC10QParser():
    pass

class SEC8KParser():
    pass