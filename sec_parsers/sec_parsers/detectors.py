
class Detector:
    def __init__(self, recursive_rule='continue',relative_rule='process',style=None,xml_rule='header',hierarchy=-1,\
                 title_tag = 'company_designated_header'):
        self.recursive_rule = recursive_rule # 'return' or 'continue'
        self.relative_rule = relative_rule # 'process' or 'ignore'. Determine whether relative parser is applied
        self.hierarchy = hierarchy # 'header','text','ignore','base_header' base header is appended to document
        self.style = style
        self.title_tag = title_tag 
        self.xml_rule = xml_rule # header, text, ignore

class StyleTagDetector(Detector):
    def __init__(self, style=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style