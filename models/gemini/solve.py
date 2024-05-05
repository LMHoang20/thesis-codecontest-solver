import datasets

from huggingface_hub import login
from inference import get_db_conn
from model import Gemini
from constants import *
from datetime import datetime
from logger import get_logger

def get_dataset_from_hf():
	login(HF_READ_TOKEN)
	dataset = datasets.load_dataset(EDITORIAL_DATASET, split='train', cache_dir='cache-editorial') 
	# dataset = dataset.filter(lambda x: x['has_code'])
	return dataset

def create_table_solve_attempts():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS solve_attempts (
		id SERIAL PRIMARY KEY,
		name TEXT NOT NULL,
		content TEXT NOT NULL,
		judge_result TEXT,
		session_id TIMESTAMP
	)
	''')
	conn.commit()
	cursor.close()

def insert_solve_attempt(name, content, session_id):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	INSERT INTO solve_attempts (name, content, session_id)
	VALUES (%s, %s, %s)
	''', (name, content, session_id))
	conn.commit()
	cursor.close()

def make_prompt_solve(name, description, tags): 
	return f"""You are a contestant in a competitive programming problem. You are given the following problem statement. Your task is to solve the problem.

You must solve the problem in a long, and detailed step-by-step manner. Must follow these steps:
- Read the problem statement carefully. Explain the reason behind the given test input and test output. For example, for the input 6, the output is 3 because we need 3 consecutive numbers to add up to 6, that is [1, 2, 3], because 1 + 2 + 3 = 6. Write out the constraints of the problem and make comment about what space/time complexity would be acceptable. For example, if the input size is 10^5, then the time complexity must be O(nlogn) or better.
- Make a detailed reasoning about the problem statement. Make some claims, observations about the problem. For example, claim that the problem can be solved greedily because it is always optimal to do X, it is never optimal to do Y; claim that the problem can be solved with dynamic programming, define the states, transitions, calculate top-down/bottom-up; claim that the problem can be modeled as a graph problem, define the vertices, and edges, etc. Write out the math if necessary.
- Plan what you are going to do to solve the problem. What mathematical, DSA concepts you are going to use. Analyze the space and time complexity of your plan, explain how that complexity is reasonable on modern computer, assuming the time limit is 2 seconds and memory limit is 512MB.
- Explain how the plan should be executed by actually calculating the result (numbers, or texts) of each step on the given test input and output of the problem.
- Implement the plan in cpp or python. Your implemetation must follow the plan closely, and must be correct.

Your output must be in the format:
# INPUT-OUTPUT-EXPLANATION:
{{your explanation of the input and output of the problem}}
# PROBLEM-REASONING:
{{your reasoning about the problem. Each observation/fact/mathematical/DSA reasoning must be in a separate bullet point}}
# PROBLEM-PLANNING:
{{your step-by-step plan. Each step must be in a separate bullet point}}
# EXECUTION-BY-HAND:
{{how your plan is executed on the test input and output of the problem}}
# IMPLEMENTATION:
```cpp or py
{{your implementation}}
```

Here is the problem statement:
# Name: {name}
# Tags: {tags}
# Description:
{description}
"""

def good(content):
	indices = [
		content.find('# INPUT-OUTPUT-EXPLANATION:'),
		content.find('# PROBLEM-REASONING:'),
		content.find('# PROBLEM-PLANNING:'),
		content.find('# EXECUTION-BY-HAND:'),
		content.find('# IMPLEMENTATION:')
	]
	return -1 not in indices and indices == sorted(indices)

if __name__ == '__main__':
	model = Gemini()
	dataset = get_dataset_from_hf()
	print(dataset)
	create_table_solve_attempts()
	start_doing = False
	while True:
		session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/solve.log', 'threadsafe': False})
		for sample in dataset:
			if sample['name'].startswith('269_B'):
				start_doing = True
			if not start_doing:
				continue
			logger.info(f'Generating content for problem {sample["name"]}')
			prompt = make_prompt_solve(sample['name'], sample['description'], sample['tags'])
			try:
				content = model.generate_content(prompt)
				if not good(content):
					raise Exception('Content is not good')
				print(content)
				insert_solve_attempt(sample['name'], content, session_id)
				logger.info(f'Generated content for problem {sample["name"]}')
			except Exception as e:
				logger.error(f'Error generating content for problem {sample["name"]}: {e}')

	
