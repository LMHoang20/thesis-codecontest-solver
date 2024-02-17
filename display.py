import json

from constants import *

urls = set()

with open(CLEAN_EDITORIAL_CONTENT_PATH, 'r') as file:
    for i, line in enumerate(file):
        data = json.loads(line)
        if data['url'] in urls:
            continue
        urls.add(data['url'])
        with open(f"data/raw_markdowns/{i}.md", 'w') as out:
            out.write(data['content'])
