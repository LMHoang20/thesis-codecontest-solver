import os
import unicodedata

for root, dirs, files in os.walk('data/md'):
    files = sorted(files)
    for file in files:
        file_dir = os.path.join(root, file)
        with open(file_dir, 'r') as f:
            content = f.read()
        first_line = content.split('\n')[0]
        try:
            for c in content:
                c.encode('ascii')
        except UnicodeEncodeError as e:
            print(e)
            print(f'{file_dir} has non-ascii characters')
        if content.count('## Description:') == 0:
            print(f'{file_dir} has no Description')
        if content.count('## Solution:') == 0:
            print(f'{file_dir} has no Editorial')
        if content.count('## Code:') == 0:
            print(f'{file_dir} has no code')
