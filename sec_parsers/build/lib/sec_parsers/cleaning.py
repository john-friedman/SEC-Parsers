import re

# Module to clean the text

# TODO
# add cleaning scripts here
# need more details on what they are used on
def clean_text(text):
    text = text.strip()
    return text

def clean_tag_name(text):
    text = text.lower()
    text = re.sub('\s+', '', text)
    return text