
class Detector:
    def __init__(self, recursive_rule='continue',relative_rule='process',style=None):
        self.recursive_rule = recursive_rule # 'return' or 'continue'
        self.relative_rule = relative_rule # 'process' or 'skip'
        self.parsing_rule = 'parse' # 'parse' or 'skip' WIP
        self.style = style

class StyleTagDetector(Detector):
    def __init__(self, style=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style