10K Parser Timeline
1. Parser that read html as text and guessed if a string was a header or paragraph.
* used manual inspection to verify if parsing was correct.
2. Various parsers that used detect unique text (e.g. bold, italic, etc) to guess what was a header / section
* Worked pretty well, but got too complex, so rewrote. 
3. Table of Contents Parser (stable) - parser that read the table of contents and used the links inside to form the skeleton of the xml tree
* Worked well: [stats]. However, decided to use lessons learned to try a new approach
4. Parser that uses visible style to construct tree.
* This will be hard. Lots of edge cases such as pART I (caps denote bold), etc
* use line breaks. use understanding of sec standardized structure.
* use relative style (e.g. one element to another) to decide parents and children.

Logic: (check other ideas first)
is item connected to other element (use to cleanup eg pART)
is item by itself (e.g. not in paragraph), LHS
calculate and keep track of style for parent / children
if so -> heading
else --> text

how to handle text directly under part or item
as text? or as new <item>?

add metadata at some point


