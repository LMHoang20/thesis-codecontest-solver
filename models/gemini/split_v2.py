import os

from model import Gemini

MAX_INPUT_TOKEN = 30720
MAX_OUTPUT_TOKEN = 2048

def get_few_shot():
    result = ''
    with open('models/gemini/split_v2/context.md', 'r') as f:
        context = f.read()
    for i in range(1, 5):
        with open(f'models/gemini/split_v2/few-shot-{i}.md', 'r') as f:
            prompt = f.read()
            result += context + '\n' + prompt + '\n'
    return result + context + '\n'

def get(content, tag):
    start_tag = f'<{tag}-START>'
    end_tag = f'<{tag}-END>'
    return content[content.find(start_tag) + len(start_tag):content.find(end_tag)].strip()

def generate(contest_id, few_shot):
    file = f'data/prompts/{contest_id}/editorial.md'    
    with open(file, 'r') as f:
        content = f.read()
        editorial = get(content, 'EDITORIAL')
        required = get(content, 'REQUIRED')
        problems = [p[p.find('.')+2:] for p in required.split('\n')]
        for problem in problems:
            if problem not in editorial:
                return 'not obvious'
    prompt = few_shot + f'\n<EDITORIAL>\n{editorial}\n</EDITORIAL>\n'
    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if '<ANSWER-START>' not in text or '<ANSWER-END>' not in text:
                token_count = model.count_tokens(prompt).total_tokens
                if token_count >= MAX_INPUT_TOKEN:
                    return 'input too long'
                token_count = model.count_tokens(text).total_tokens
                if token_count >= MAX_OUTPUT_TOKEN:
                    return 'output too long'
            answer = get(text, 'ANSWER')
            titles = answer.split('\n')
            indices = [editorial.find(title) for title in titles]
            if not all(i != -1 for i in indices):
                continue
            if not all(indices[i] < indices[i+1] for i in range(len(indices)-1)):
                continue
            with open(f'data/prompts/{contest_id}/editorial-generated.md', 'w') as f:
                f.write(response.text)
            return 'ok'
        except:
            token_count = model.count_tokens(prompt).total_tokens
            if token_count >= MAX_INPUT_TOKEN:
                return 'input too long'
            token_count = model.count_tokens(text).total_tokens
            if token_count >= MAX_OUTPUT_TOKEN:
                return 'output too long'
    else:
        return 'error'

def filter_dir(dir):
    return '-' not in dir and int(dir) in range(71, 1155)

if __name__ == '__main__':
    model = Gemini()
    few_shot = get_few_shot()
    dirs = [f for f in os.listdir('data/prompts/') if filter_dir(f)]
    dirs = sorted(dirs, key=lambda x: int(x))
    for contest_id in dirs:
        print(contest_id, end=' ', flush=True)
        result = generate(contest_id, few_shot)
        print(result)
        with open(f'review-1.txt', 'a') as f:
            f.write(f'{contest_id}: {result}\n')