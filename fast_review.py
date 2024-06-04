import os

from logger import get_logger

file_dict = {}

for root, _, files in os.walk('data/corrected'):
    files = sorted(files, reverse=True)

for file in files:
    file = file[:-3]
    name = '-'.join(file.split('-')[:2])
    if name not in file_dict:
        file_dict[name] = {}
    if file.endswith('-corrected'):
        file_dict[name]['corrected'] = f'{file}.md'
    elif file.endswith('-corrected-gemini'):
        file_dict[name]['corrected'] = f'{file}.md'
    elif file.endswith('-reviewed'):
        file_dict[name]['reviewed'] = f'{file}.md'
    else:
        file_dict[name]['original'] = f'{file}.md'

files = sorted(list(file_dict.items()), key=lambda x: (int(x[0].split('-')[0]), x[0].split('-')[1]))
for x in files:
    if 'reviewed' in x[1]:
        with open(f'data/corrected/{x[1]["reviewed"]}', 'r') as f:
            content = f.read()
            if '\\wedge' in content:
                path = f'data/corrected/{x[1]["reviewed"]}'
                print(path)
        continue
    print(x[0])
    for version, file_name in x[1].items():
        with open(f'data/corrected/{file_name}', 'r') as f:
            content = f.read()
        with open(f'review/{version}.md', 'w') as f:
            f.write(content)
    while True:
        c = input()
        if c == 's':
            break
        elif c == 'q':
            exit()
        else:
            print('Invalid command')
    with open(f'review/corrected.md', 'r') as f:
        content = f.read()
    with open(f'data/corrected/{x[0]}-reviewed.md', 'w') as f:
        f.write(content)

    

        