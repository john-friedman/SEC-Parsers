from sec_parsers.detectors import StyleTagDetector
from sec_parsers.style_detection import detect_part,detect_item,detect_signatures,detect_page_number,detect_bullet_point,\
    detect_all_caps,detect_note,detect_emphasis_capitalization


class EmptyStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='empty;',**kwargs)

    def detect(self,string):
        if string.strip() == '':
            return 'empty;'
        else:
            return ''

class PartStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='part;',**kwargs)

    def detect(self,string):
        if detect_part(string):
            return 'part;'
        else:
            return ''
        
class ItemStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='item;',**kwargs)

    def detect(self,string):
        if detect_item(string):
            return 'item;'
        else:
            return ''
    
class SignaturesStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='signatures;',**kwargs)

    def detect(self,string):
        if detect_signatures(string):
            return 'signatures;'
        else:
            return ''
        
class PageNumberStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='page number;',**kwargs)

    def detect(self,string): 
        if detect_page_number(string):
            return 'page number;'
        else:
            return ''

class BulletPointStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='bullet point;',**kwargs)

    def detect(self,string):
        if detect_bullet_point(string):
            return 'bullet point;'
        else:
            return ''

class AllCapsStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='all caps;',**kwargs)

    def detect(self,string):
        if detect_all_caps(string):
            return 'all caps;'
        else:
            return ''

class NoteStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='note;',**kwargs)

    def detect(self,string):
        if detect_note(string):
            return 'note;'
        else:
            return ''
              

class EmphasisCapStringDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='emphasis capitalization;',**kwargs)

    def detect(self,string):
        if detect_emphasis_capitalization(string):
            return 'emphasis;'
        else:
            return ''