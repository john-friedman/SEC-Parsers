from sec_parsers.css_detectors import BoldCSSDetector, ItalicCSSDetector, UnderlineCSSDetector, HiddenCSSDetector
from sec_parsers.tag_detectors import TableTagDetector, ImageTagDetector, LinkTagDetector, BoldTagDetector, \
    StrongTagDetector, EmphasisTagDetector, ItalicTagDetector, UnderlineTagDetector, TableOfContentsTagDetector


class HeaderElementDetectorGroup:
    def __init__(self):

        self.element_detectors = []
        self.add_element_detector(HiddenCSSDetector(parsing_rule='return',cleaning_rule='remove'))
        self.add_element_detector(TableTagDetector(parsing_rule='return', cleaning_rule='skip'))
        self.add_element_detector(ImageTagDetector(parsing_rule='return', cleaning_rule='remove'))
        self.add_element_detector(LinkTagDetector(parsing_rule='return', cleaning_rule='remove')) # WIP
        self.add_element_detector(BoldTagDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(StrongTagDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(EmphasisTagDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(ItalicTagDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(UnderlineTagDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(BoldCSSDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(UnderlineCSSDetector(parsing_rule='continue', cleaning_rule='header'))
        self.add_element_detector(ItalicCSSDetector(parsing_rule='continue', cleaning_rule='header'))


    def add_element_detector(self, element_detector):
        self.element_detectors.append(element_detector)

    def insert_element_detector(self, element_detector, position):
        self.element_detectors.insert(position, element_detector)

    def detect(self,element):
        for element in self.element_detectors:
            result = element.detect(element)
            if result != '':
                return result
        return ''

class SEC10KElementGroup(HeaderElementDetectorGroup):
    def __init__(self):
        super().__init__()
        # Table of contents detector needs to go before table detector
        self.insert_element_detector(TableOfContentsTagDetector(parsing_rule ='return',cleaning_rule ='skip'),0)

class SEC8KElementGroup(SEC10KElementGroup):
    pass
