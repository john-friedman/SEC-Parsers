import re

# add cleaning scripts here

def clean_text(text):
    text = text.strip()
    return text

def clean_tag_name(text):
    text = text.lower()
    text = re.sub('\s+', '', text)
    return text