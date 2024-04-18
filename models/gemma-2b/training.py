import datasets
import gc

from inference import load_model
from settings import *
from constants import *

def format_instruction(sample):
    name = sample['name']
    description = sample['description']
    tags = sample['tags']
    editorial = sample['editorial']
    sections = editorial.split('TUTORIAL CODE XXX')
    solution = sections[0].strip()
    code = sections[1].strip()
    return f"""<start_of_turn>user
You are a contestant in a programming contest. You are given the following complicated competitive programming problem:
The problem description is given between the <DESCRIPTION> and </DESCRIPTION> tags.

Here is your task:
- Reason about the problem, write the editorial for the problem, wrapped in the <EDITORIAL> and </EDITORIAL> tags.
- Write a solution in any programming language, preferably in Python/C++, wrapped in the <CODE> and </CODE> tags.

Your entire answer should be wrapped in the <ANSWER> and </ANSWER> tags. Answer in Markdown format.

<DESCRIPTION>
Name: {name}
Tags: {tags}
{description}
</DESCRIPTION><end_of_turn>
<start_of_turn>model
<ANSWER>
<EDITORIAL>
{solution}
</EDITORIAL>
<CODE>
{code}
</CODE>
</ANSWER><end_of_turn>"""
    

if __name__ == "__main__":
    model, tokenizer = load_model()

    DATASET_ID = EDITORIAL_DATASET
    SPLIT = 'train'
    CACHE_DIR = 'cache-editorial'

    dataset = datasets.load_dataset(DATASET_ID)

    dataset = dataset.filter(lambda x: x['has_code'])
    
    print(format_instruction(dataset['train'][0]))

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        max_seq_length=max_seq_length,
        tokenizer=tokenizer,
        packing=packing,
        formatting_func=format_instruction,
        args=args,
    )        

    gc.collect()
    trainer.train()