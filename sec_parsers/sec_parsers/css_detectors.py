from detectors import Detector
from sec_parsers.style_detection import detect_hidden_element, detect_bold_from_css, detect_underline_from_css, detect_italic_from_css

class HiddenCSSDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,element):
        if detect_hidden_element(element):
            return 'hidden;'
        else:
            return ''
        
class BoldCSSDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,element):
        if detect_bold_from_css(element):
            return 'bold;'
        else:
            return ''
        
class UnderlineCSSDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,element):
        if detect_underline_from_css(element):
            return 'underline;'
        else:
            return ''
        
class ItalicCSSDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def detect(self,element):
        if detect_italic_from_css(element):
            return 'italic;'
        else:
            return ''