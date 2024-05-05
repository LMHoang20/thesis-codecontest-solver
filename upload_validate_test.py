import helpers
import datasets

from huggingface_hub import login
from database import get_db_conn
from entity.problem import Problem
from constants import *

def transform_columns(dataset):
    dataset_dict = {
        'name': [],
        'description': [],
        'tags': [],
        'rating': [],
        'source': [],
        'editorial': [],
    }
    for sample in dataset:
        assert sample['source'] == 2
        dataset_dict['name'].append(sample['name'])
        dataset_dict['description'].append(sample['description'])
        dataset_dict['tags'].append(', '.join(sample['cf_tags']))
        dataset_dict['rating'].append(str(sample['cf_rating']))
        dataset_dict['source'].append('codeforces')
        dataset_dict['editorial'].append('')
    return datasets.Dataset.from_dict(dataset_dict)

def create_table_problem_validation():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS problems_v2 (
            name VARCHAR(255) PRIMARY KEY,
            description TEXT NOT NULL,
            source INT,
            difficulty INT,
            cf_contest_id INT,
            cf_index VARCHAR(255),
            cf_rating INT,
            cf_tags []TEXT,
            time_limit JSONB,
            memory_limit_bytes JSONB,
            split TEXT
        );
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_to_db(sample, split):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO testing_problems (name, description, cf_rating, cf_tags, split)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (sample['name'], sample['description'], sample['rating'], sample['tags'], split)
    )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    login(HF_WRITE_TOKEN)
    dataset_id = 'deepmind/code_contests'
    validate_set = datasets.load_dataset(dataset_id, split='valid', trust_remote_code=True, cache_dir='cache-validate')
    validate_set = transform_columns(validate_set)
    validate_set.push_to_hub('HoangLe1312/codecontest-reasoning', split='validate')
    test_set = datasets.load_dataset(dataset_id, split='test', trust_remote_code=True, cache_dir='cache-validate')
    test_set = transform_columns(test_set)
    test_set.push_to_hub('HoangLe1312/codecontest-reasoning', split='test')
    create_table_problem_validation()
    test_set = datasets.load_dataset('HoangLe1312/codecontest-reasoning', split='test', trust_remote_code=True)
    for sample in test_set:
        insert_to_db(sample, 'test')
    validate_set = datasets.load_dataset('HoangLe1312/codecontest-reasoning', split='validate', trust_remote_code=True)
    for sample in validate_set:
        insert_to_db(sample, 'validate')

    