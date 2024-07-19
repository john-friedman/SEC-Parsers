import re
# Module to store common regex patterns (move later)
# Module to clean the text

def clean_string(string):
    # Replace zero-width non-joiner
    cleaned_string = string.replace('\u200c', '')
    
    return cleaned_string


def clean_title(text): #  adjust to format items and parts into standardized format, e.g. no periods
    # preprocess
    text = clean_string(text)

    text = text.strip()
    text = re.sub("[^\S \t\n\r\f\v]+",' ',text)

    # remove line breaks
    text = re.sub('\n', ' ', text)

    # replace multiple spaces with single space
    text = re.sub('\s+', ' ', text)


    return text

def clean_string_for_style_detection(text):
    """WIP"""
    # preprocess
    text = clean_string(text)

    chars_to_remove = ['-','_']
    # remove chars_to_remove
    for char in chars_to_remove:
        text = re.sub(char,'',text)

    text = text.strip()
    return text

# common regex patterns
part_pattern = re.compile(r"^part\s+([1234]|iv|i{1,4})(?:$|\b)",re.IGNORECASE)

def is_string_in_middle(parent_text, search_string):
    index = parent_text.find(search_string)
    if index == -1:
        return False  # String not found
    
    if index == 0:
        return False  # String is at the beginning of the text
    
    char_before = parent_text[index - 1]
    return char_before != '\n' and char_before != ''


