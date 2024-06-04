import os

for root, _, files in os.walk('data/prompts'):
    for file in files:
        if file.endswith('-prompt.md-generated.md') \
            or file.endswith('-generated.md'):
            os.remove(f'{root}/{file}')