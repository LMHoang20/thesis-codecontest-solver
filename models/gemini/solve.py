import datasets
from huggingface_hub import login
from inference import get_db_conn
from model import Gemini
from constants import *

def get_dataset_from_hf():
	login(HF_READ_TOKEN)
	dataset = datasets.load_dataset(EDITORIAL_DATASET, split='train', cache_dir='cache-editorial') 
	dataset = dataset.filter(lambda x: x['has_code'])
	return dataset

def create_table_solve_attempts():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS solve_attempts (
		id SERIAL PRIMARY KEY,
		contest_id VARCHAR(10) NOT NULL,
		problem_id VARCHAR(10) NOT NULL,
		content TEXT NOT NULL,
		judge_result TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)
	''')
	conn.commit()
	cursor.close()

def insert_solve_attempt(contest, problem_id, content):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO solve_attempts (contest_id, problem_id, content)
        VALUES (%s, %s, %s)
    ''', (contest, problem_id, content))
	conn.commit()
	cursor.close()

def make_prompt_solve(name, description, tags, editorial, code, multiple_code = False): 
	return f"""<TASK>
</TASK>
"""

if __name__ == '__main__':
	model = Gemini()
	dataset = get_dataset_from_hf()
	create_table_solve_attempts()
	
