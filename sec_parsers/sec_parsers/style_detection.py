import re
# since we need styles that are non standardized this will be fun

def detect_style(string):
    def detect_emphasis_capitalization(string):
        """Seen in amazon's 2024 10k e.g. We Have Foreign Exchange Risk"""
        words = string.split()
        if not words:
            return False
        for word in words:
            if word.lower() in ["of",'to','a','and']:
                continue
            if not word[0].isupper():
                return False
        return True
    
    def detect_item(string):
        """e.g. Item 1A. Risk Factors"""
        match = re.search(r"^Item\s+\d+[A-Z]",string)
        if match:
            return True

    
    if detect_emphasis_capitalization(string):
        return 'emphasis'
    elif detect_item(string):
        return 'item'
    else:
        return 'no style found'