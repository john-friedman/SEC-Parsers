from sec_parsers.detectors import HiddenElementDetector, TableElementDetector, ImageElementDetector
from sec_parsers.detector_groups import HeaderStringDetectorGroup
from sec_parsers.xml_helper import get_text

class HTMLParser:
    def __init__(self):
        self.detectors = []
        self.add_detector(HiddenElementDetector())
        self.add_detector(TableElementDetector())
        self.add_detector(ImageElementDetector())

        self.string_detector = HeaderStringDetectorGroup()

    
    def add_detector(self, detector):
        self.detectors.append(detector)

    def recursive_parse(self, element):
        for detector in self.detectors:
            result = detector.detect(element)
            if result != '':
                element.attrib['parsing_string'] = result
                return
            
        text = get_text(element).strip()
        if text == '':
            for child in element.iterchildren():
                self.recursive_parse(child)
        else:
            # handle string detection
            # some strings when found should trigger return
            # other should continue to element detection

            # handle element detection
            # logic for adding to element or parent element
            pass




class SEC10KStringDetector:
    pass

# should inherit htmlparser and add filing stuff
class FilingParser:
    pass

class SEC10KParser:
    pass
