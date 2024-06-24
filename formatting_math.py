import os

l = []

for root, _, files in os.walk('data/corrected'):
    for file in files:
        if 'reviewed' not in file:
            continue
        with open(f'{root}/{file}', 'r') as f:
            content = f.read()
        if '<=' in content and '```' not in content:
            l.append(f'{root}/{file}')

l = sorted(l)
for x in l:
    print(x)