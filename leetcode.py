import os
import json
import unicodedata

from transformers import AutoTokenizer

def normalize_text(text):
    ascii_char = [char for char in text if ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z')]
    return ''.join(ascii_char)

def load_tokenizer():
    model_id = "unsloth/Phi-3-medium-4k-instruct-bnb-4bit"
    tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="cache-phi-tokenizer")
    return tokenizer

def get_editorials():
    pass

def format_leetcode():
    pass

def get_leetcode():
    solutions = {}
    descriptions = {}
    for root, _, files in os.walk('./data/leetcode'):
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for file in files:
            if not file.endswith('.json'):
                continue
            path = f'{root}/{file}'
            with open(path, 'r') as f:
                problem = json.load(f)
                title, description, solution = problem['title'], problem['description'], problem['solution']
                if title.startswith('256 -'):
                    print(title)
                    print(description)
                    print(solution)
                    exit(0)
                    continue
                lines = solution.split('\n')
                lines = [line.rstrip() for line in lines if line.strip() != '']
                if len(lines) <= 1:
                    continue
                solution = unicodedata.normalize('NFKD', solution)
                # replaces = {
                #     '«': '<<',
                #     '\u200b': ' ',
                #     '»': '>>',
                #     '—': '-',
                #     '–': '-',
                #     'é': 'e',
                # }
                # for key, value in replaces.items():
                #     solution = solution.replace(key, value)
                if '## Code:' in solution:
                    solution = solution.split('## Code:')[0]
                if solution not in solutions:
                    solutions[solution] = title
                else:
                    print(title)
                    print(solutions[solution])
                    print(solution)
                    print('----------------')
                descriptions[title] = description
    sus = []
    for solution, title in solutions.items():
        if title == '1250 - Check If It Is a Good Array':
            continue
        index = title.split('-')[0][:-1]
        if not os.path.exists(f'./data/md/{index}.md'):
            continue
        with open(f'./data/md/{index}.md', 'r') as f:
            content = f.read()
            if normalize_text(solution) not in normalize_text(content):
                sus.append(title)
    solutions = [(title, solution) for solution, title in solutions.items()]
    print(len(solutions))
    print(sus)
    
def get_math():
    pass

if __name__ == '__main__':
    get_leetcode()
    get_math()
    get_editorials()
    format_leetcode()
    # load_tokenizer()