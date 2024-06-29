# SEC Parsers

## What it does
Converts SEC filings into well structured xml trees.

## Design Principles
1. Avoid Complexity - complexity slows down iteratition speed, makes it hard to apply principles elsewhere
2. Good Visualization - visualization allows identification of erros quickly
3. Run-time only needs to be as fast as is useful for improving parser

## Problem
SEC filings are easily human readable but not machine readable. E.g. a human can look at an SEC 10-K filing and easily figure out what sections are subsections, e.g. Part, then item, then seasonality etc, but machines have trouble.

## Existing Approaches
1. Regex
2. ML
3. OCR

## How SEC Parsers is different:
1. Capability: SEC Parsers parses all headings, not just parts and items.
2. Approach: Uses the relational structure in html (e.g. tags like <b> <div>) alongside regex to construct the xml tree

## How SEC Parsers work:

### Parsers

### Visualization

### Convert to XML

## How non-standardized are SEC filings: (add screenshots)
1. Headers can be disguised as table tags
2. middle text issue <p> text1 <span>text2</span> text3</p>
3. random letter bolded e.g. pART I
4. headers style various across 10Ks
5. headers text are sometimes split between tags

## List of existing alternatives
1. sec-parser 
2. sec-api (paid)
3. https://www.textblocks.app/
4. notre dame
5. R package




