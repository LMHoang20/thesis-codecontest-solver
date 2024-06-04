import helpers
import datasets

from psycopg2.extras import Json
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
        'solutions': []
    }
    for sample in dataset:
        assert sample['source'] == 2
        dataset_dict['name'].append(sample['name'])
        dataset_dict['description'].append(sample['description'])
        dataset_dict['tags'].append(', '.join(sample['cf_tags']))
        dataset_dict['rating'].append(str(sample['cf_rating']))
        dataset_dict['source'].append('codeforces')
        dataset_dict['editorial'].append('')
        dataset_dict['solutions'].append(sample['solutions'])
    return datasets.Dataset.from_dict(dataset_dict)

def create_table_testing_problems():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS testing_problems;
        CREATE TABLE IF NOT EXISTS testing_problems (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            public_tests JSONB NOT NULL,
            private_tests JSONB NOT NULL,
            generated_tests JSONB NOT NULL,
            solutions JSONB,
            cf_contest_id INT NOT NULL,
            cf_index TEXT NOT NULL,
            cf_rating INT NOT NULL,
            cf_tags TEXT NOT NULL,
            split TEXT NOT NULL
        )
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
        INSERT INTO testing_problems (name, description, public_tests, private_tests, generated_tests, cf_contest_id, cf_index, cf_rating, cf_tags, split, solutions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (sample['name'], sample['description'], Json(sample['public_tests']), Json(sample['private_tests']), Json(sample['generated_tests']), sample['cf_contest_id'], sample['cf_index'], str(sample['cf_rating']), ', '.join(sample['cf_tags']), split, Json(sample['solutions']))
    )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    login(HF_WRITE_TOKEN)
    dataset_id = 'deepmind/code_contests'
    validate_set = datasets.load_dataset(dataset_id, split='valid', trust_remote_code=True, cache_dir='cache-validate')
    # validate_set = transform_columns(validate_set)
    # validate_set.push_to_hub('HoangLe1312/codecontest-reasoning', split='validate')
    test_set = datasets.load_dataset(dataset_id, split='test', trust_remote_code=True, cache_dir='cache-validate')
    # test_set = transform_columns(test_set)
    # test_set.push_to_hub('HoangLe1312/codecontest-reasoning', split='test')
    create_table_testing_problems()
    # test_set = datasets.load_dataset('HoangLe1312/codecontest-reasoning', split='test', trust_remote_code=True)
    for sample in test_set:
        insert_to_db(sample, 'test')
    # validate_set = datasets.load_dataset('HoangLe1312/codecontest-reasoning', split='validate', trust_remote_code=True)
    for sample in validate_set:
        insert_to_db(sample, 'validate')

    