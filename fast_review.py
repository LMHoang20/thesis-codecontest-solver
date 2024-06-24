import os

from logger import get_logger

file_dict = {}

# for root, _, files in os.walk('data/corrected'):
#     files = sorted(files, reverse=True)

# for file in files:
#     file = file[:-3]
#     name = '-'.join(file.split('-')[:2])
#     if name not in file_dict:
#         file_dict[name] = {}
#     if file.endswith('-corrected'):
#         file_dict[name]['corrected'] = f'{file}.md'
#     elif file.endswith('-corrected-gemini'):
#         file_dict[name]['corrected'] = f'{file}.md'
#     elif file.endswith('-reviewed'):
#         file_dict[name]['reviewed'] = f'{file}.md'
#     else:
#         file_dict[name]['original'] = f'{file}.md'

for _, dirs, _ in os.walk('data/contests-extra'):
    for dir in dirs:
        if 'skip' in dir:
            continue
        if '_' not in dir:
            continue
        for root, _, files in os.walk(f'data/contests-extra/{dir}'):
            for file in files:
                if 'skip' in file:
                    continue
                if 'editorial' in file:
                    continue
                file = file[:-3]
                contest = dir.split('_')[0]
                problem = file.split('-')[0]
                name = f'{contest}-{problem}'
                path = f'data/contests-extra/{dir}/{file}.md'
                if name not in file_dict:
                    file_dict[name] = {}
                if file.endswith('-corrected'):
                    file_dict[name]['corrected'] = path
                else:
                    file_dict[name]['original'] = path

files = sorted(list(file_dict.items()), key=lambda x: (int(x[0].split('-')[0]), x[0].split('-')[1]))

for x in files:
    if 'reviewed' in x[1]:
        continue
    print(x[0])
    for version, file_name in x[1].items():
        if file_name.startswith('data'):
            path = file_name
        else:
            path = f'data/corrected/{file_name}'
        with open(path, 'r') as f:
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

    

        