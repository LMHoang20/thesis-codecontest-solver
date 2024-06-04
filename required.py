import os

os.mkdir('data/required')

for root, dirs, files in os.walk('data/prompts'):
    for file in files:
        if file != 'editorial.md':
            continue
        with open(os.path.join(root, file), 'r') as f:
            content = f.read()
            if '<REQUIRED-START>' in content and '<REQUIRED-END>' in content:
                required = content[content.find('<REQUIRED-START>') + len('<REQUIRED-START>'):content.find('<REQUIRED-END>')].strip()
                print(required)
                contest_id = os.path.basename(root)
                with open(f'data/required/{contest_id}.md', 'w') as f:
                    f.write(required)
        