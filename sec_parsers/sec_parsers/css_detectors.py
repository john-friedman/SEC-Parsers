from sec_parsers.detectors import StyleTagDetector
from sec_parsers.style_detection import detect_hidden_element, detect_bold_from_css, detect_underline_from_css, detect_italic_from_css

class HiddenCSSDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='hidden',**kwargs)

    def detect(self,element):
        if detect_hidden_element(element):
            return 'hidden'
        else:
            return ''
        
class BoldCSSDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='bold',**kwargs)

    def detect(self,element):
        if detect_bold_from_css(element):
            return 'bold'
        else:
            return ''
        
class UnderlineCSSDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='underline',**kwargs)

    def detect(self,element):
        if detect_underline_from_css(element):
            return 'underline'
        else:
            return ''
        
class ItalicCSSDetector(StyleTagDetector):
    def __init__(self, **kwargs):
        super().__init__(style='italic',**kwargs)

    def detect(self,element):
        if detect_italic_from_css(element):
            return 'italic'
        else:
            return ''