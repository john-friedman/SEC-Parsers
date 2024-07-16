from sec_parsers.tag_detectors import TableTagDetector, ImageTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text

class HTMLParser:
    def __init__(self):
        self.element_detectors = [] # e.g. table image link etc
        self.add_element_detector(HiddenCSSDetector(parsing_rule='return'))
        self.add_element_detector(TableTagDetector(parsing_rule='return'))
        self.add_element_detector(ImageTagDetector(parsing_rule='return'))

        self.string_detector = HeaderStringDetectorGroup() # strings that should be detected
        self.tag_dectectors = []
        self.css_detectors = []
        self.style_detectors = self.css_detectors + self.tag_dectectors # e.g. strong, emphasis, italic, underline, etc

    
    def add_element_detector(self, element_detector):
        self.element_detectors.append(element_detector)

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





class SEC10KStringDetector:
    pass

# should inherit htmlparser and add filing stuff
class FilingParser:
    pass

class SEC10KParser:
    pass
