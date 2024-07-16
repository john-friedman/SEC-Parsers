from sec_parsers.detectors import Detector
from sec_parsers.style_detection import detect_part,detect_item,detect_signatures,detect_page_number,detect_bullet_point,\
    detect_all_caps,detect_note,detect_emphasis_capitalization


class PartStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_part(string):
            return 'part;'
        else:
            return ''
        
class ItemStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_item(string):
            return 'item;'
        else:
            return ''
    
class SignaturesStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_signatures(string):
            return 'signatures;'
        else:
            return ''
        
class PageNumberStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string): 
        if detect_page_number(string):
            return 'page number;'
        else:
            return ''

class BulletPointStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_bullet_point(string):
            return 'bullet point;'
        else:
            return ''

class AllCapsStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_all_caps(string):
            return 'all caps;'
        else:
            return ''

class NoteStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_note(string):
            return 'note;'
        else:
            return ''
              

class EmphasisCapStringDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,string):
        if detect_emphasis_capitalization(string):
            return 'emphasis;'
        else:
            return ''