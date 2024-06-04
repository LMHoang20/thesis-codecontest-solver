import helpers
import yaml
import asyncio

from huggingface_hub import login
from database import get_db_conn
from entity.problem import Problem
from models import Gemini
from constants import *

def get_match_code(name):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT code, language
	FROM matches
	WHERE name = %s
	ORDER BY score DESC, session_id DESC
	LIMIT 1
	""", (name,))
	match = cursor.fetchone()
	cursor.close()
	code = match[0]
	language = int(match[1])
	if language in [1, 3]:
		code = f'```py\n{code}\n```'
	elif language in [2]:
		code = f'```cpp\n{code}\n```'
	elif language in [4]:
		code = f'```java\n{code}\n```'
	assert code.startswith('```')
	return code

def get_problem_editorial(name):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name, p.description, p.cf_tags, p.cf_rating, e.content, e.solutions
	FROM problems p
	JOIN editorials e ON p.name = e.name
	WHERE p.name = %s
	""", (name,))
	problem = cursor.fetchone()
	cursor.close()
	editorial = problem[4]
	while '<REMOVE-THIS>' in editorial:
		assert editorial.find('<REMOVE-THIS>') < editorial.find('</REMOVE-THIS>')
		remove_start = editorial.find('<REMOVE-THIS>')
		remove_end = editorial.find('</REMOVE-THIS>') + len('</REMOVE-THIS>')
		editorial = editorial[:remove_start] + editorial[remove_end:]
	editorial = helpers.normalize_editorial(editorial)
	codes = problem[5]
	if codes:
		code = codes[0]
	else:
		code = get_match_code(name)
	return Problem(name=problem[0], description=problem[1], editorial=editorial, code=code, tags=problem[2], rating=problem[3], source='codeforces')

def get_problem_names():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name
	FROM problems p
	JOIN editorials e ON p.name = e.name
	""")
	problems = cursor.fetchall()
	conn.close()
	return problems

def get_prompt(problem: Problem):
	task = """System:
You are given a problem statement, and the editorial for the problem.
The editorial has been automatically separated into sentences, each on a new line.
But the editorial might not be separated correctly. 
You need to identify the whether the sentences are separated correctly or not.
If not, you need to provide the correct separation.
"""
	problem_statement = f"""Problem statement:
{problem.name}
Description:
{problem.description}
Editorial:
{problem.editorial}
"""
	output_format = """You MUST answer in the following format:
```yaml
---
analysis: |
    <check the correctness of the editorial separation>
conclusion: YES/NO
corrected: |
    <if NO, provide the corrected editorial>
```
"""
	return [task, problem_statement, output_format]

if __name__ == '__main__':
	model = Gemini()
	names = get_problem_names()
	with open('checked.txt', 'r') as f:
		checked = f.readlines()
		checked = [name.strip() for name in checked]
		names = [name for name in names if name[0] not in checked]
	if True:
		for name in names:
			name = name[0]
			print(name)
			problem = get_problem_editorial(name)
			if '*special' in problem.tags:
				continue
			prompt = get_prompt(problem)
			response = model.generate(prompt)
			if response.startswith("```yaml"):
				response = response[7:]
			if response.endswith("```"):
				response = response[:-3]
			response = yaml.safe_load(response)
			conclusion = response['conclusion']
			if not conclusion:
				with open('reviewwwwwww.txt', 'a') as f:
					f.write(f'{problem.name}\n')
					f.write('---------------SMALL-SEP---------------')
					f.write(f'{problem.editorial}\n')
					f.write('---------------SMALL-SEP---------------')
					f.write(f'{response["corrected"]}\n')
					f.write('---------------SEP---------------')
			with open('checked.txt', 'a') as f:
				f.write(f'{problem.name}\n')
