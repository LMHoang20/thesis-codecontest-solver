import psycopg2
import datasets
import json

from huggingface_hub import login
from psycopg2.extras import Json
from constants import *

create_table_sql = '''
CREATE TABLE problems (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  description TEXT NOT NULL,
  public_tests JSONB NOT NULL,
  private_tests JSONB NOT NULL,
  generated_tests JSONB NOT NULL,
  source INT NOT NULL,
  difficulty INT NOT NULL,
  solutions JSONB NOT NULL,
  incorrect_solutions JSONB NOT NULL,
  cf_contest_id INT NOT NULL,
  cf_index VARCHAR(255) NOT NULL,
  cf_points FLOAT NOT NULL,
  cf_rating INT NOT NULL,
  cf_tags text[] NOT NULL,
  is_description_translated BOOLEAN NOT NULL,
  untranslated_description TEXT NOT NULL,
  time_limit JSONB,
  memory_limit_bytes INT NOT NULL,
  input_file TEXT NOT NULL,
  output_file TEXT NOT NULL,
  editorial TEXT NOT NULL
);
'''

login(HF_READ_TOKEN)

dataset_name = 'deepmind/code_contests'
split = 'train'
cache_dir = 'cache'

dataset = datasets.load_dataset(dataset_name, split=split, cache_dir=cache_dir)

conn = psycopg2.connect(
   database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432'
)

conn.autocommit = True

review = open('review.txt', 'w')

for sample in dataset:
    editorial = ''
    file = f'data/contests/{sample["cf_contest_id"]}-done/{sample["cf_index"]}.md'
    if os.path.exists(file):
        with open(file, 'r') as f:
            editorial = f.read()
            print(file)
    cur = conn.cursor()
    try:
        cur.execute(f'''
    INSERT INTO problems 
    (name, description, public_tests, private_tests, generated_tests, 
    source, difficulty, solutions, incorrect_solutions, 
    cf_contest_id, cf_index, cf_points, cf_rating, cf_tags,
    is_description_translated, untranslated_description, 
    time_limit, memory_limit_bytes,
    input_file, output_file, editorial)
    VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s,
    %s, %s,
    %s, %s, %s
    )''', [
        sample['name'],
        sample['description'],
        Json(sample['public_tests']),
        Json(sample['private_tests']),
        Json(sample['generated_tests']),
        sample['source'],
        sample['difficulty'],
        Json(sample['solutions']),
        Json(sample['incorrect_solutions']),
        sample['cf_contest_id'],
        sample['cf_index'],
        sample['cf_points'],
        sample['cf_rating'],
        sample['cf_tags'],
        sample['is_description_translated'],
        sample['untranslated_description'],
        Json(sample['time_limit']),
        sample['memory_limit_bytes'],
        sample['input_file'],
        sample['output_file'],
        editorial    
    ])
    except Exception as e:
        review.write(f'{sample["cf_contest_id"]}-{sample["cf_index"]}\n')
    cur.close()

conn.close()
review.close()