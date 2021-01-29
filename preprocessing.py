from pathlib import Path # available in python 3.4 +

import pandas as pd
Genre_dir = r'data/responses_csv/Genre Movies' # raw string for windows.
Languages_dir = r'data/responses_csv/Languages'
Others_dir = r'data/responses_csv'


dir = Others_dir
csv_files = [f for f in Path(dir).glob('*.csv')] # finds all csvs in your folder.

data = ''


for csv in csv_files: #iterate list
    with open(csv, 'r', encoding="utf-8") as file:
        data = file.read().replace('"', "").replace(",", "")

    with open(csv, 'w', encoding="utf-8") as file:
        file.write(data)
