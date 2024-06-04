import os
import google.generativeai as genai
import time

for root, dirs, files in os.walk('data/contests-extra'):
    for dir in dirs:
        if 'skip' in dir:
            continue
        if 'generated' not in dir:
            continue
        for root, _, files in os.walk(f'data/contests-extra/{dir}'):
            for file in files:
                if '-' in file:
                    continue
                if 'editorial' in file:
                    continue
                if 'corrected' in file:
                    continue
                with open(f'{root}/{file}', 'r') as f:
                    content = f.read()
                if 'TUTORIAL CODE XXX' in content:
                    content = content.split('TUTORIAL CODE XXX')[0]
                token_count = genai.count_message_tokens(prompt=content)['token_count']
                if token_count > 1000:
                    print(f'{root}/{file}', token_count)
                    continue
                tts = 60/90 + 0.1
                time.sleep(tts)