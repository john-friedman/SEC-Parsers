from sec_parsers.string_detectors import AllCapsStringDetector, EmphasisCapStringDetector, PageNumberStringDetector, BulletPointStringDetector, NoteStringDetector,\
      PartStringDetector, ItemStringDetector, SignaturesStringDetector, NoteStringDetector
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
    
class SEC10KStringDetectorGroup(HeaderStringDetectorGroup):
    def __init__(self):
        super().__init__()
        
        # Add part, item, and signatures detectors at the beginning
        new_detectors = [
            PartStringDetector(parsing_rule='return',level=0,cleaning_rule='header;'),
            ItemStringDetector(parsing_rule='return',level=1,cleaning_rule='header;'),
            SignaturesStringDetector(parsing_rule='return',level=0,cleaning_rule='header;'),
            NoteStringDetector(parsing_rule='continue',cleaning_rule='header;'),
            PageNumberStringDetector(parsing_rule='continue',cleaning_rule='remove;'),
            BulletPointStringDetector(parsing_rule='continue',cleaning_rule='skip;')
        ]
        self.insert_string_detectors(new_detectors)
        
class SEC8KStringDetectorGroup(HeaderStringDetectorGroup):
    def __init__(self):
        super().__init__()
        
        # Add part, item, and signatures detectors at the beginning
        new_detectors = [
            ItemStringDetector(parsing_rule='return',level=0,cleaning_rule='header;'),
            SignaturesStringDetector(parsing_rule='return',level=0,cleaning_rule='header;'),
            NoteStringDetector(parsing_rule='continue',cleaning_rule='header;'),
            PageNumberStringDetector(parsing_rule='continue',cleaning_rule='remove;'),
            BulletPointStringDetector(parsing_rule='continue',cleaning_rule='skip;')
        ]
        self.insert_string_detectors(new_detectors)
        