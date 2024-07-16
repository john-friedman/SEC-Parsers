from sec_parsers.detectors import Detector, StyleTagDetector
from sec_parsers.style_detection import detect_link,detect_bold_from_html,detect_strong_from_html,detect_emphasis_from_html,\
    detect_italic_from_html,detect_underline_from_html,detect_table,detect_table_of_contents,detect_image




class LinkTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='link', **kwargs)

    def detect(self,element):
        if detect_link(element):
            return 'link;'
        else:
            return ''
        
class BoldTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='bold', **kwargs)

    def detect(self,element):
        if detect_bold_from_html(element):
            return 'bold;'
        else:
            return ''

class StrongTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style ='strong', **kwargs)

    def detect(self,element):
        if detect_strong_from_html(element):
            return 'strong;'
        else:
            return ''
        
class EmphasisTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='emphasis',**kwargs)

    def detect(self,element):
        if detect_emphasis_from_html(element):
            return 'emphasis;'
        else:
            return ''
        
class ItalicTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='italic',**kwargs)

    def detect(self,element):
        if detect_italic_from_html(element):
            return 'italic;'
        else:
            return ''

class UnderlineTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='underline',**kwargs)

    def detect(self,element):
        if detect_underline_from_html(element):
            return 'underline;'
        else:
            return ''
        

        
class TableTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='table',**kwargs)

    def detect(self,element):
        if detect_table(element):
            return 'table;'
        
        return ''
        
class TableOfContentsTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='table',**kwargs)

    def detect(self,element):
        if detect_table(element):
            if detect_table_of_contents(element) == "toc":
                return 'table of contents;'
            
        return ''
        
class ImageTagDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='image', **kwargs)

    def detect(self,element):
        if detect_image(element):
            return 'image;'
        else:
            return ''
        