import os
import datasets
from huggingface_hub import login
from constants import *

login(HF_READ_TOKEN)
dataset_id = 'HoangLe1312/codecontest-editorials'
dataset = datasets.load_dataset(dataset_id)

data = dataset['train']

os.makedirs('./data', exist_ok=True)
os.makedirs('./data/test-contests', exist_ok=True)
for contest in data:
    if contest['note']:
        folder = './data/test-contests/' + contest['contest'] + '-' + contest['note']
    else:
        folder = './data/test-contests/' + contest['contest']
    os.makedirs(folder, exist_ok=True)
    with open(folder + '/editorial.md', 'w') as f:
        f.write(contest['editorial'])
    for problem in contest['problems']:
        if problem['note']:
            p_file = folder + '/' + problem['index'] + '-' + problem['note'] + '.md'
        else:
            p_file = folder + '/' + problem['index'] + '.md'
        with open(p_file, 'w') as f:
            f.write(problem['content'])


            