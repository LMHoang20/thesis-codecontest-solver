import datasets

from huggingface_hub import login
from constants import *

login(HF_READ_TOKEN)

dataset_name = 'deepmind/code_contests'
split = 'train'
cache_dir = 'cache'

dataset = datasets.load_dataset(dataset_name, split=split, cache_dir=cache_dir)


def filter_function(sample):
    return sample['source'] == 2 and \
        len(sample['public_tests']['input']) > 0 and \
        len(sample['private_tests']['input']) > 0 and \
        len(sample['solutions']) > 0 and \
        len(sample['incorrect_solutions']) > 0 and \
        sample['cf_contest_id'] > 0 and \
        sample['cf_index'] != '' and \
        sample['input_file'] == '' and \
        sample['output_file'] == ''


dataset = dataset.filter(filter_function)

for sample in dataset:
    os.makedirs(f'data/description/{sample["cf_contest_id"]}', exist_ok=True)
    with open(f'data/description/{sample["cf_contest_id"]}/{sample["cf_index"]}.md', 'w') as f:
        f.write(f'# {sample["cf_index"]}: {sample["name"]}\n\n')
        f.write(f'## Description\n\n')
        f.write(sample['description'])