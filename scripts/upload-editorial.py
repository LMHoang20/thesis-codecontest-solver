import os
import datasets
from huggingface_hub import login
from constants import *

data = []
for root, dirs, files in os.walk('./data/contests'):
    for dir in dirs:
        if '-' in dir:
            contest = dir.split('-')[0]
            note = dir[len(contest)+1:]
        else:
            contest = dir
            note = None
        editorial = ''
        problems = []
        for root, dirs, files in os.walk('./data/contests/' + dir):
            for file in files:
                if file == 'editorial.md':
                    with open('./data/contests/' + dir + '/editorial.md', 'r') as f:
                        editorial = f.read()
                else:
                    if '-' in file:
                        p_index = file.split('-')[0]
                        p_note = file[len(p_index)+1:]
                    else:
                        p_index = file
                        p_note = None
                    content = ''
                    with open('./data/contests/' + dir + '/' + file, 'r') as f:
                        content = f.read()
                    problems.append({
                        'index': p_index,
                        'note': p_note,
                        'content': content
                    })
        data.append({
            'contest': contest,
            'note': note,
            'editorial': editorial,
            'problems': problems
        })

dataset_id = 'HoangLe1312/codecontest-editorials'
dataset = datasets.Dataset.from_dict({
    'contest': [x['contest'] for x in data],
    'note': [x['note'] for x in data],
    'editorial': [x['editorial'] for x in data],
    'problems': [x['problems'] for x in data]
})

login(HF_WRITE_TOKEN)
dataset.push_to_hub(dataset_id)