# %%
import datasets

# %%
# from constants import *
from huggingface_hub import login
from constants import *

login(HF_READ_TOKEN)

# %%
dataset_name = 'deepmind/code_contests'
split = 'train'
cache_dir = 'cache'

dataset = datasets.load_dataset(dataset_name, split=split, cache_dir=cache_dir)

def filter_function(sample):
    return sample['source'] == 2 and \
        len(sample['public_tests']['input']) > 0 and \
        len(sample['private_tests']['input']) > 0 and \
        sample['cf_contest_id'] > 0 and \
        sample['cf_index'] != '' and \
        sample['input_file'] == '' and \
        sample['output_file'] == ''

dataset = dataset.filter(filter_function)

# %%
print(dataset)

# %%
# with open(PROBLEM_URLS_PATH, 'w') as f:
    # for sample in dataset:
        # url = f"https://codeforces.com/problemset/problem/{sample['cf_contest_id']}/{sample['cf_index']}"
        # f.write(url + '\n')

# %%
contest_ids = set()
for sample in dataset:
    contest_ids.add(sample['cf_contest_id'])

print(len(contest_ids))

# %%



