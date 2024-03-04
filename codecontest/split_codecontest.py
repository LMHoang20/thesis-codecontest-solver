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

print(dataset)

language_dict = {
    0: "any",
    1: "python2",
    2: "cpp",
    3: "python3",
    4: "java",
}

def format(language, code, correct):
    return f"""### Settings:
Language: {language_dict[language]}
Correct: {correct}
Editorial: False

### Code:
{code}
"""

def augment(samples):
    prompts = []
    indices = []
    contests = []

    for contest, index, solutions, incorrect_solutions \
    in zip(samples["cf_contest_id"], samples["cf_index"], samples["solutions"], samples["incorrect_solutions"]):
        correct_prompt = [
            format(language, code, True) 
            for language, code 
            in zip(
                solutions["language"], 
                solutions["solution"]
            ) 
        ]
            
        incorrect_prompt = [
            format(language, code, False) 
            for language, code 
            in zip(
                incorrect_solutions["language"], 
                incorrect_solutions["solution"]
            )
        ]
            
        cnt = len(correct_prompt) + len(incorrect_prompt)
        contests += [contest] * cnt
        indices += [index] * cnt
        prompts += correct_prompt + incorrect_prompt
    
    return {
        "contest": contests,
        "index": indices,
        "prompt": prompts
    }

dataset = dataset.map(augment, batched=True, remove_columns=dataset.column_names)

print(dataset)

login(HF_WRITE_TOKEN)

my_dataset_hf_repo = 'HoangLe1312/codecontest-prompt'

dataset.push_to_hub(my_dataset_hf_repo)