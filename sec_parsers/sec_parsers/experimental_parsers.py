from sec_parsers.tag_detectors import LinkTagDetector, BoldTagDetector, StrongTagDetector, EmphasisTagDetector, ItalicTagDetector,\
      UnderlineTagDetector, TableTagDetector, ImageTagDetector, TableOfContentsTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector, BoldCSSDetector,UnderlineCSSDetector,ItalicCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup, SEC10KStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text

# need to remember to ignore hidden css in relative parsing

class HTMLParser:
    def __init__(self):
        self.element_detectors = [] # e.g. table image link etc
        self.add_element_detector(HiddenCSSDetector(parsing_rule='return'))
        self.add_element_detector(TableTagDetector(parsing_rule='return'))
        self.add_element_detector(ImageTagDetector(parsing_rule='return'))

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
            parsing_string_found = False
            for detector in self.string_detector.string_detectors:
                result = detector.detect(text)
                if result != '':
                    if detector.parsing_rule == 'return':
                        # e.g. for items, parts, etc
                        parsing_string = result
                        parsing_string_found = True
                        break  # Break the loop instead of returning
                    elif detector.parsing_rule == 'continue':
                        parsing_string += result # WIP, not sure what to think about this?
                        parsing_string_found = True

            if not parsing_string_found:
                # other should continue to style detectors
                for detector in self.style_detectors:
                    result = detector.detect(element)
                    if result != '':
                        parsing_string += detector.style + ';'

                # check parsing string is not empty
                if parsing_string == '':
                    return

            # logic for adding to element or parent element, may want to move later
            if element.tail is not None: # WIP think about this
                parent = element.getparent()
                parent.attrib['parsing_string'] = parsing_string + 'parent;'
            else:
                element.attrib['parsing_string'] = parsing_string
        return
    
    def relative_parse(self,html):
        # WIP
        pass


class SEC10KParser(HTMLParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.insert_element_detector(TableOfContentsTagDetector(),0) # change to right before table detector 
        self.string_detector = SEC10KStringDetectorGroup() #WIP

 
class SEC10QParser():
    pass

class SEC8KParser():
    pass