import datasets
from constants import *
from huggingface_hub import login

if __name__ == '__main__':
    # dataset_id = 'hendrycks/competition_math'
    dataset_id = 'HoangLe1312/codecontest-reasoning'
    dataset = datasets.load_dataset(dataset_id, split='train', trust_remote_code=True)
    print(dataset[123]['description'])