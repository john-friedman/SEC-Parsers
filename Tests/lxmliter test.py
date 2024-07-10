from lxml import etree

# Sample HTML content
html_content = """
<div>
    <p id="first">First paragraph.</p>
    <p id="second">Second paragraph.</p>
    <p id="third">Third paragraph.</p>
</div>
"""

# Parse the HTML content
tree = etree.HTML(html_content)

# Find the element whose previous sibling you want to get
element = tree.xpath('//p[@id="second"]')[0]

# Get the previous sibling
previous_sibling = element.getprevious()

# Print the previous sibling's text
if previous_sibling is not None:
    print(etree.tostring(previous_sibling, pretty_print=True).decode('utf-8'))
else:
    print("No previous sibling found.")
