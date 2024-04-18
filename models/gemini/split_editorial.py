import pathlib
import google.generativeai as genai
import psycopg2
import threading

from judge import judge
from huggingface_hub import login

from IPython.display import display
from IPython.display import Markdown

from constants import *
from model import Gemini

def get_few_shot():
    result = ''
    with open('models/gemini/split_prompts/task.md', 'r') as f:
        task = f.read()
    for i in range(1, 5):
        with open(f'models/gemini/split_prompts/few-shot-{i}.md', 'r') as f:
            prompt = f.read()
            result += task + '\n' + prompt + '\n'
    return result + task + '\n'

def generate(dir):
    print(dir, 'START')
    with open(dir, 'r') as f:
        prompt = f.read()
    target = prompt[prompt.find('<TARGET>') + len('<TARGET>'):prompt.find('</TARGET>')].strip()
    target = target[len('problem name: '):]
    editorial = prompt[prompt.find('<EDITORIAL>') + len('<EDITORIAL>'):prompt.find('</EDITORIAL>')].strip()
    if target not in editorial:
        with open(f'{dir}-generated.md', 'w') as f:
            f.write('<ANSWER>\nNO SOLUTION\n</ANSWER>')
        return
    for _ in range(3):
        try:
            response = model.generate_content(few_shot + prompt)
            text = response.text.strip()
            if '<ANSWER>' not in text or '</ANSWER>' not in text:
                continue
            text = text[text.find('<ANSWER>') + len('<ANSWER>'):text.find('</ANSWER>')].strip()
            if text != 'NO SOLUTION':
                text = text[text.find('<TUTORIAL>') + len('<TUTORIAL>'):text.find('</TUTORIAL>')].strip()
                if text not in prompt:
                    continue
            dir = dir[:dir.find('-prompt')]
            with open(f'{dir}-generated.md', 'w') as f:
                f.write(response.text)
            print(dir, 'OK')
            return
        except:
            pass
    else:
        dir = dir[:dir.find('-prompt')]
        with open(f'{dir}-generated.md', 'w') as f:
            f.write('<ANSWER>\nNO SOLUTION\n</ANSWER>')
        print(dir, 'ERROR')
    

if __name__ == '__main__':
    model = Gemini()
    few_shot = get_few_shot()
    for root, _, files in os.walk('data/prompts/'):
        for file in files:
            if '-generated' in file:
                continue
            if '-prompt' not in file:
                continue
            dir = f'{root}/{file}'
            generate(dir)