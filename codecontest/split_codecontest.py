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
        sample['cf_contest_id'] > 0 and \
        sample['cf_index'] != '' and \
        sample['input_file'] == '' and \
        sample['output_file'] == ''

dataset = dataset.filter(filter_function)

dataset = dataset[:10]

print(dataset)

language_dict = {
    0: "any",
    1: "python2",
    2: "cpp",
    3: "python3",
    4: "java",
}

def format(description, language, code, correct):
    return f"""### Instruction:
You are a contestant in a programming contest on Codeforces. You have to solve the problem described below.

### Description:
{description}

### Settings:
Language: {language_dict[language]}
Correct: {correct} 

### Code:
{code}
"""

def augment(sample):
    print(sample)
    print(sample['solutions'])
    print(type(sample['solutions']))
    correct_solutions = [
        format(sample['description'], language, code, True) 
        for language, code 
        in zip(
            sample["solutions"]["language"], 
            sample["solutions"]["solution"]
        )
    ]
    incorrect_solutions = [
        format(sample['description'], language, code, False) 
        for language, code 
        in zip(
            sample["incorrect_solutions"]["language"], 
            sample["incorrect_solutions"]["solution"])
    ]
    cnt = len(correct_solutions) + len(incorrect_solutions)
    id = f"{sample['cf_contest_id']}-{sample['cf_index']}"
    return {
        "id": [id] * cnt,
        "prompt": correct_solutions + incorrect_solutions,
    }

dataset = dataset.map(augment, batched=True, remove_columns=dataset.column_names)

login(HF_WRITE_TOKEN)

my_dataset_hf_repo = 'HoangLe1312/codecontest-prompt'

dataset.push_to_hub(my_dataset_hf_repo)