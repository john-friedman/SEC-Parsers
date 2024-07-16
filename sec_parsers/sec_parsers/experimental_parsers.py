from sec_parsers.tag_detectors import TableTagDetector, ImageTagDetector
from sec_parsers.css_detectors import HiddenCSSDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup
from sec_parsers.xml_helper import get_text

class HTMLParser:
    def __init__(self):
        self.element_detectors = []
        self.add_element_detector(HiddenCSSDetector(parsing_rule='return'))
        self.add_element_detector(TableTagDetector(parsing_rule='return'))
        self.add_element_detector(ImageTagDetector(parsing_rule='return'))

        self.string_detector = HeaderStringDetectorGroup()
        self.html_dectectors = []
        self.css_detectors = []
        self.style_detectors = self.css_detectors + self.html_detectors

    
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
            for detector in self.string_detector.string_detectors:
                result = detector.detect(text)
                if result != '':
                    if detector.parsing_rule == 'return':
                        # e.g. for items, parts, etc
                        element.attrib['parsing_string'] = result
                        return
                    elif detector.parsing_rule == 'continue':
                        parsing_string += result

            
                # other should continue to element detection

                # handle element detection

                # logic for adding to element or parent element




class SEC10KStringDetector:
    pass

# should inherit htmlparser and add filing stuff
class FilingParser:
    pass

class SEC10KParser:
    pass
