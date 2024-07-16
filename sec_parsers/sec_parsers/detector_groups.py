from sec_parsers.css_detectors import HiddenCSSDetector
from sec_parsers.tag_detectors import TableTagDetector, ImageTagDetector
from sec_parsers.string_detectors import AllCapsStringDetector, EmphasisCapStringDetector, PageNumberStringDetector, BulletPointStringDetector, NoteStringDetector, PartStringDetector, ItemStringDetector, SignaturesStringDetector
from sec_parsers.cleaning import clean_string_for_style_detection

class HeaderStringDetectorGroup:
    def __init__(self):
        self.string_detectors = []
        self.add_string_detector(AllCapsStringDetector())
        self.add_string_detector(EmphasisCapStringDetector())

    def add_string_detector(self, string_detector):
        self.string_detectors.append(string_detector)

    def insert_string_detectors(self, string_detectors):
        """Inserts string detectors list into first position"""
        self.string_detectors = string_detectors + self.string_detectors

    def detect(self,string):
        string = clean_string_for_style_detection(string)
        for string_detector in self.string_detectors:
            result = string_detector.detect(string)
            if result != '':
                return result
        return ''
    
class FilingStringDetectorGroup(HeaderStringDetectorGroup):
    def __init__(self):
        super().__init__()
        
        # Add part, item, and signatures detectors at the beginning
        new_detectors = [
            PartStringDetector(parsing_rule='return'),
            ItemStringDetector(parsing_rule='return'),
            SignaturesStringDetector(parsing_rule='return')
        ]
        self.insert_string_detectors(new_detectors)
        
        # Add page number, bullet point, and note detectors at the end
        self.add_string_detector(PageNumberStringDetector())
        self.add_string_detector(BulletPointStringDetector())
        self.add_string_detector(NoteStringDetector())