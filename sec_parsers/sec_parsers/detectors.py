from sec_parsers.style_detection import detect_hidden_element,detect_emphasis_capitalization,detect_table,detect_table_of_contents,\
    detect_image,detect_part,detect_item,detect_signatures,detect_page_number,detect_bullet_point,detect_all_caps,detect_note

class Detector:
    def __init__(self, parsing_rule='continue'):
        self.parsing_rule = parsing_rule

# Element Detectors

class HiddenElementDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,element):
        if detect_hidden_element(element):
            return 'hidden;'
        else:
            return ''
        
class TableElementDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,element):
        if detect_table(element):
            if detect_table_of_contents(element) == "toc":
                return 'table of contents;'
            else:
                return 'table;'
        else:
            return ''
        
class ImageElementDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,element):
        if detect_image(element):
            return 'image;'
        else:
            return ''
        
# String Detectors
        
class PartStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_part(string):
            return 'part;'
        else:
            return ''
        
class ItemStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_item(string):
            return 'item;'
        else:
            return ''
    
class SignaturesStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_signatures(string):
            return 'signatures;'
        else:
            return ''
        
class PageNumberStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string): 
        if detect_page_number(string):
            return 'page number;'
        else:
            return ''

class BulletPointStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_bullet_point(string):
            return 'bullet point;'
        else:
            return ''

class AllCapsStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_all_caps(string):
            return 'all caps;'
        else:
            return ''

class NoteStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_note(string):
            return 'note;'
        else:
            return ''
              

class EmphasisCapStringDetector(Detector):
    def __init__(self):
        super().__init__()

    def detect(self,string):
        if detect_emphasis_capitalization(string):
            return 'emphasis;'
        else:
            return ''