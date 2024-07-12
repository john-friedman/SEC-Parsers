import re
# Module to clean the text


def clean_title(text): #  adjust to format items and parts into standardized format, e.g. no periods
    text = text.strip()
    text = re.sub("[^\S \t\n\r\f\v]+",' ',text)

    # remove line breaks
    text = re.sub('\n', ' ', text)

    # replace multiple spaces with single space
    text = re.sub('\s+', ' ', text)

    return text

def clean_string_for_style_detection(text):
    """WIP"""
    chars_to_remove = ['-','_']
    # remove chars_to_remove
    for char in chars_to_remove:
        text = re.sub(char,'',text)

    text = text.strip()
    return text