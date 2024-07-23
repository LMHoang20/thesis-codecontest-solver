import repository

from transformers import AutoTokenizer
from database import get_db_conn
from helpers import remove_consecutive_line_breaks
from matplotlib import pyplot as plt
import datasets
from huggingface_hub import login
from constants import HF_WRITE_TOKEN

def get_editorials(split):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, description, editorial, solutions, split
        FROM cleaned_editorials
        WHERE split = %s
        ORDER BY name
    """, (split,))
    editorials = cursor.fetchall()
    conn.close()
    return editorials

mini_model_id = "unsloth/Phi-3-mini-4k-instruct-bnb-4bit"
mini_tokenizer = AutoTokenizer.from_pretrained(mini_model_id, cache_dir="cache-phi-mini-tokenizer")
# print(mini_tokenizer(['<|user|>'], return_tensors = 'pt'))
# print(mini_tokenizer(['<|assistant|>'], return_tensors = 'pt'))
# print(mini_tokenizer(['<|end|>'], return_tensors = 'pt'))
# '<|endoftext|>'
# print(mini_tokenizer.eos_token)

medium_model_id = "unsloth/Phi-3-medium-4k-instruct-bnb-4bit"
medium_tokenizer = AutoTokenizer.from_pretrained(medium_model_id, cache_dir="cache-phi-medium-tokenizer")

problem_repo = repository.Problem(get_db_conn())

def normalize(text):
    text = remove_consecutive_line_breaks(text.strip()).strip()
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    text = '\n'.join(lines)
    return text

def format_prompt(name, tags, rating, description, editorial, tokenizer):
    if type(tags) == list:
        tags = ', '.join(tags)
    assert type(tags) == str or tags is None
    user_prompt = f"""
You are a professional competitive programmer, solve the following problem in natural language.
Name: {name}
{f"Tags: {tags}" if tags else ""}
{f"Rating: {rating}" if rating else ""}
Description:
{description}
"""
    model_answer = editorial
    prompt = tokenizer.apply_chat_template([
        {"role": "user", "content": normalize(user_prompt)},
        {"role": "assistant", "content": normalize(model_answer)}
    ], tokenize = False, add_generation_prompt = False).strip()
    if not prompt.endswith(tokenizer.eos_token):
        prompt += tokenizer.eos_token
    token_count = tokenizer(prompt, return_length = True)['length']
    return prompt, token_count[0]

def get_example(editorial):
    name, description, editorial, solutions, split = editorial
    if split != 'leetcode':
        problem = problem_repo.get_problem(name)
        assert problem is not None
        tags = problem.tags
        rating = problem.rating
    else:
        tags = None
        rating = None
    mini_prompt, mini_token_count = format_prompt(name, tags, rating, description, editorial, mini_tokenizer)
    medium_prompt, medium_token_count = format_prompt(name, tags, rating, description, editorial, medium_tokenizer)
    # assert mini_prompt == medium_prompt, (mini_prompt, medium_prompt)
    # assert mini_token_count == 2 + medium_token_count, (mini_token_count, medium_token_count)
    return mini_prompt, mini_token_count, medium_prompt, medium_token_count

def main():
    train_set = get_editorials('train')
    validate_set = get_editorials('validate')
    leetcode_set = get_editorials('leetcode')
    test_set = get_editorials('test')
    print(len(train_set), len(validate_set), len(leetcode_set), len(test_set))
    # train_example, token_count = get_example(train_set[0])
    # print(train_example)
    # print(token_count)
    # validate_example, token_count = get_example(validate_set[0])
    # print(validate_example)
    # print(token_count)
    # leetcode_example, token_count = get_example(leetcode_set[0])
    # print(leetcode_example)
    # print(token_count)
    train_dataset = {
        'mini_prompt': [],
        'mini_token_count': [],
        'medium_prompt': [],
        'medium_token_count': []
    }
    validate_dataset = {
        'mini_prompt': [],
        'mini_token_count': [],
        'medium_prompt': [],
        'medium_token_count': []
    }
    test_dataset = {
        'mini_prompt': [],
        'mini_token_count': [],
        'medium_prompt': [],
        'medium_token_count': []
    }
    train_token_counts = []
    validate_token_counts = []
    test_token_counts = []
    train_names = []
    validate_names = []
    test_names = []

    for editorial in train_set:
        train_names.append(editorial[0])
        mini_prompt, mini_token_count, medium_prompt, medium_token_count = get_example(editorial)
        train_dataset['mini_prompt'].append(mini_prompt)
        train_dataset['mini_token_count'].append(mini_token_count)
        train_dataset['medium_prompt'].append(medium_prompt)
        train_dataset['medium_token_count'].append(medium_token_count)
        train_token_counts.append(mini_token_count)
    for editorial in validate_set:
        validate_names.append(editorial[0])
        mini_prompt, mini_token_count, medium_prompt, medium_token_count = get_example(editorial)
        validate_dataset['mini_prompt'].append(mini_prompt)
        validate_dataset['mini_token_count'].append(mini_token_count)
        validate_dataset['medium_prompt'].append(medium_prompt)
        validate_dataset['medium_token_count'].append(medium_token_count)
        validate_token_counts.append(mini_token_count)

    leetcode_tokens = 0
    for editorial in leetcode_set:
        train_names.append(editorial[0])
        mini_prompt, mini_token_count, medium_prompt, medium_token_count = get_example(editorial)
        train_dataset['mini_prompt'].append(mini_prompt)
        train_dataset['mini_token_count'].append(mini_token_count)
        train_dataset['medium_prompt'].append(medium_prompt)
        train_dataset['medium_token_count'].append(medium_token_count)
        train_token_counts.append(mini_token_count)
        leetcode_tokens += mini_token_count
    for editorial in test_set:
        test_names.append(editorial[0])
        mini_prompt, mini_token_count, medium_prompt, medium_token_count = get_example(editorial)
        test_dataset['mini_prompt'].append(mini_prompt)
        test_dataset['mini_token_count'].append(mini_token_count)
        test_dataset['medium_prompt'].append(medium_prompt)
        test_dataset['medium_token_count'].append(medium_token_count)
        test_token_counts.append(mini_token_count)
    assert len(train_names) == len(set(train_names)), len(train_names)
    assert len(validate_names) == len(set(validate_names)), len(validate_names)
    assert len(test_names) == len(set(test_names)), len(test_names)
    assert not any(name in validate_names or name in test_names for name in train_names)
    assert not any(name in train_names or name in test_names for name in validate_names)
    assert not any(name in train_names or name in validate_names for name in test_names)
    print(len(train_dataset['mini_prompt']), len(validate_dataset['mini_prompt']), len(test_dataset['mini_prompt']))
    print(sum(train_token_counts) - leetcode_tokens, leetcode_tokens, sum(validate_token_counts), sum(test_token_counts))
    print(max(train_token_counts), max(validate_token_counts), max(test_token_counts))
    print(min(train_token_counts), min(validate_token_counts), min(test_token_counts))
    plt.hist(train_token_counts, bins = 100)
    plt.xlabel('Token Count')
    plt.ylabel('Frequency')
    plt.title('Token Count Distribution')
    plt.show()
    plt.hist(validate_token_counts, bins = 20)
    plt.xlabel('Token Count')
    plt.ylabel('Frequency')
    plt.title('Token Count Distribution')
    plt.show()
    # login(HF_WRITE_TOKEN)
    # train_dataset = datasets.Dataset.from_dict(train_dataset)
    # train_dataset.push_to_hub("cleaned-editorials", split="train")
    # validate_dataset = datasets.Dataset.from_dict(validate_dataset)
    # validate_dataset.push_to_hub("cleaned-editorials", split="validate")
    # test_dataset = datasets.Dataset.from_dict(test_dataset)
    # test_dataset.push_to_hub("cleaned-editorials", split="test")

if __name__ == '__main__':
    main()
