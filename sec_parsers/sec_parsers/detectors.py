
class Detector:
    def __init__(self, recursive_rule='continue',relative_rule='process'):
        self.recursive_rule = recursive_rule
        self.relative_rule = relative_rule

class StyleTagDetector(Detector):
    def __init__(self, style=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style