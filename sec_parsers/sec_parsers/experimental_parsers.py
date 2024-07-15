from sec_parsers.detectors import HiddenElementDetector, TableElementDetector, ImageElementDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup
from sec_parsers.xml_helper import get_text

class HTMLParser:
    def __init__(self):
        self.detectors = []
        self.add_detector(HiddenElementDetector(parsing_rule='return'))
        self.add_detector(TableElementDetector(parsing_rule='return'))
        self.add_detector(ImageElementDetector(parsing_rule='return'))

        self.string_detector = HeaderStringDetectorGroup()

    
    def add_detector(self, detector):
        self.detectors.append(detector)

    def recursive_parse(self, element):
        for detector in self.detectors:
            result = detector.detect(element)
            if result != '':
                if parsing_rule == 'return':
                    element.attrib['parsing_string'] = result
                    return
            
        text = get_text(element).strip()
        if text == '':
            for child in element.iterchildren():
                self.recursive_parse(child)
        else:
            for string_detector in self.string_detector.string_detectors:
                parsing_string = string_detector.detect(text)
                parsing_rule = string_detector.parsing_rule

                if parsing_string != '':
                    if parsing_rule == 'return':
                        element.attrib['parsing_string'] = parsing_string
                        return
                    elif parsing_rule == 'continue':
                        pass

            
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
