    # tests for checking if the table of contents was read correctly

    import bs4
    import pandas as pd
    import re
    from download import download_sec_filing

    from html_helper import get_table_of_contents, open_soup, detect_table_of_contents

    dir_10k = "../../Data/10K/"

    # get list of files
    import os
    files = os.listdir(dir_10k)
    files = [dir_10k + file for file in files]

    correct_idx = 0
    # ../../Data/10K/1004724_0000950170-24-039414.html not working - missing a link (mistake on their end) - have to fix, not sure how
    # '../../Data/10K/1008586_0001493152-24-017297.html' - no toc
    # ../../Data/10K/1017655_0001437749-24-010365.html toc but no links
    for idx,file in enumerate(files):
        if idx < correct_idx:
            continue
        
        print(f"{idx}: {file}")
        with open(file, 'r', encoding='utf-8-sig') as f:
            html = f.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        toc_dict = get_table_of_contents(soup)

        # Extracting the relevant information and creating a DataFrame
        records = []
        for part in toc_dict['parts']:
            for item in part['items']:
                records.append({
                    'part': part['name'],
                    'item': item['name'],
                    'desc': item['desc'],
                    # 'item_href': item['href'],
                    # 'part_href': part['href'],
                })

        df = pd.DataFrame(records)
        print(df)
        
        open_soup(soup)
        confirmation = input("Does this look correct? (press y to confirm)")

        if confirmation == 'y':  # Check for an empty string (Enter key press)
            print("Confirmed!")
        else:
            print("You entered something:", confirmation)
