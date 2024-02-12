import os
from dotenv import load_dotenv
import json

load_dotenv()

EDITORIAL_URLS_PATH = os.getenv('EDITORIAL_URLS_PATH')

EDITORIAL_POSSIBLE_TITLES = [
    'editorial',
    'tutorial',
    'разбор',
    't (en)',
    'e (en)'
]

BLACK_LIST = [
    'ru',
    'announcement',
    'annoucement',
]

no_material = []
no_editorial = []
editorial_urls = []
special_cases = []

def extract_editorial_urls(results):
    urls = []
    for result in results:
        result_title = result['title'].lower()
        for title in EDITORIAL_POSSIBLE_TITLES:
            if title not in result_title:
                continue
            if any(black_list in result_title for black_list in BLACK_LIST):
                continue
            if '.pdf' in result['url']:
                continue
            if 'blog/entry' not in result['url']:
                continue
            urls.append(result['url'])
    return urls

with open(EDITORIAL_URLS_PATH, 'r') as file:
    for line in file:
        data = json.loads(line)
        results = data['result']

        if len(results) == 0:
            no_material.append(data)
            continue

        urls = extract_editorial_urls(results)

        if len(urls) == 1:
            editorial_urls.append({
                "url": data['url'],
                "editorial_url": urls[0]
            })
        elif len(urls) == 0:
            no_editorial.append(data)
        else:
            special_cases.append(data)
            

with open('potentially-no-editorial.txt', 'w') as file:
    for data in no_editorial:
        json.dump(data, file)
        file.write('\n')

with open('potentially-no-material.txt', 'w') as file:
    for data in no_material:
        json.dump(data, file)
        file.write('\n')

with open('editorial_urls.txt', 'w') as file:
    for data in editorial_urls:
        json.dump(data, file)
        file.write('\n')

with open('special_cases.txt', 'w') as file:
    for data in special_cases:
        json.dump(data, file)
        file.write('\n')