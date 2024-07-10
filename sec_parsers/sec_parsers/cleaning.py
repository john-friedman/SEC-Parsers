import re

# Module to clean the text

# TODO

# NEW
# e.g. ITEM 1. BUSINESS --> item1, overview --> overview, Our Products and Services --> our_products_and_services

def clean_title(text):
    # add detection for item / other sections
    text = text.strip()
    if 'item' in text:
        text = re.sub('\s+', ' ', text)
    return text

# OLD
# WIP
def clean_text(text):
    text = text.strip()
    return text

# WIP
def clean_tag_name(text):
    text = text.lower()
    text = re.sub('\s+', '', text)
    return text