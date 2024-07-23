import datasets

from huggingface_hub import login
from constants import *

login(HF_WRITE_TOKEN)

dataset_id = "HoangLe1312/cleaned-editorials"
train_dataset = datasets.load_dataset(dataset_id, split = 'train')
validate_dataset = datasets.load_dataset(dataset_id, split = 'validate')

print(len(train_dataset), len(validate_dataset))
print(train_dataset)
print(validate_dataset)
print(train_dataset[0]['mini_prompt'])

# for sample in dataset:
#     print(sample['prompt'])

# prog_synthesis_dataset = datasets.load_dataset("NTU-NLP-sg/xCodeEval", "program_synthesis", ignore_verifications=True, cache_dir='xcodeeval')

# print(prog_synthesis_dataset)