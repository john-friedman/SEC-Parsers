
class Detector:
    def __init__(self,parsing_rule='continue',cleaning_rule='header', level = -1):
        self.parsing_rule = parsing_rule # 'return' - marks element as when found to return, 'continue' - marks element as when found to continue
        self.cleaning_rule = cleaning_rule # remove - elem will not be processed in xml, skip- elem will be processed, header - elem will be processed as header
        self.level = level # level of the element in the hierarchy, -1 means no level assigned

class StyleTagDetector(Detector):
    def __init__(self, style=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style # not implemented yet, idea is that e.g. for font weight we can assign 'bold' as group name