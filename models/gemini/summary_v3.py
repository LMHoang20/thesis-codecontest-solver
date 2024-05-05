import helpers

from model import Gemini
from constants import *
from match_code import get_db_conn
from logger import get_logger
from entity.problem import Problem
# from solver.train.coder import Coder
from sandbox import CppSandbox, PythonSandbox


def get_problem_names():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name
	FROM problems p
	JOIN editorials e ON p.name = e.name
	LEFT JOIN summaries_v3 s ON p.name = s.name
	WHERE s.name IS NULL
	ORDER BY p.cf_rating ASC
	""")
	problems = cursor.fetchall()
	conn.close()
	return problems

def create_table_summary_v3():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS summaries_v3 (
		name TEXT PRIMARY KEY,
		content TEXT NOT NULL,
		problem_understanding TEXT,
		solution_reasoning TEXT,
		implementation_planning TEXT,
		session_id TIMESTAMP
	)
	''')
	conn.commit()
	cursor.close()

def insert_summary_v3(name, content, problem_understanding, solution_reasoning, implementation_planning, session_id):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	INSERT INTO summaries_v3 (name, content, problem_understanding, solution_reasoning, implementation_planning, session_id)
	VALUES (%s, %s, %s, %s, %s, %s)
	""", (name, content, problem_understanding, solution_reasoning, implementation_planning, session_id))
	conn.commit()
	cursor.close()

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
	return match

def get_problem(name):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name, p.description, e.content, e.solutions, p.public_tests, p.private_tests, p.generated_tests, cf_tags, cf_rating, p.solutions
	FROM problems p
	JOIN editorials e ON p.name = e.name
	WHERE p.name = %s
	""", (name,))
	problem = cursor.fetchone()
	cursor.close()
	editorial = problem[2]
	while '<REMOVE-THIS>' in editorial:
		remove_start = editorial.find('<REMOVE-THIS>')
		remove_end = editorial.find('</REMOVE-THIS>') + len('</REMOVE-THIS>')
		editorial = editorial[:remove_start] + editorial[remove_end:]
	if len(problem[3]) > 0:
		code = problem[3][0]
	else:
		code, language = get_match_code(name)
		if language in [1, 3]:
			code = f'```py\n{code}\n```'
		elif language in [2]:
			code = f'```cpp\n{code}\n```'
	return Problem(name=problem[0], description=problem[1], editorial=editorial, code=code, public_tests=problem[4], private_tests=problem[5], generated_tests=problem[6], tags=problem[7], rating=problem[8], source='codeforces')

task = """
# Task:
Given a competitive programming problem statement and the editorial (an editorial is a solution written in natural language) for the problem.
You are required to re-write, re-structure, re-orgainze the editorial in a more structured format.
You have to rewrite the editorial as thoughts of someone who is solving the problem for the first time themselves.
"""

requirement = """
# What you MUST do 3 tasks:
- PROBLEM-UNDERSTANDING: From the problem statement, extract the key ideas, requirements, constraints, etc. from the problem statement.
- SOLUTION-REASONING: From the editorial, extract the idea observations, math-work, assumptions, conclusions, examples, etc.
- IMPLEMENTATION-PLANNING: From the code solution, plan the steps to solve the problem. The steps should be high level, skip unimportant details. Focus on unusual logic, data structures, etc.
- For each task:
	- Output in a bullet-point format.
	- The answer MUST be long, detailed, and complete. Important information MUST be included.
	- MUST have a reason for each bullet point.
	- MUST surround mathematical expressions with $ symbol.
	- MUST have between 10-20 bullet points for each task.
	- Fix any grammatical errors, spelling mistakes, etc.
"""

answer_format = """
# Answer Format:
// START OF FORMAT
PROBLEM-UNDERSTANDING:
- <sentence>. REASON: <why you extracted this sentence>
- <sentence>. REASON: <why you extracted this sentence>
- ...
SOLUTION-REASONING:
- <observation>. REASON: <why you extracted this observation>
- <observation>. REASON: <why you extracted this observation>
- ...
IMPLEMENTATION-PLANNING:
- <high-level description of the action>
- <high-level description of the action>
- ...
// END OF FORMAT
"""

problem_statement = """
# Problem Statement:
Name: {}
Tags: {}
Rating: {}
Description:
// START OF PROBLEM DESCRIPTION
{}
// END OF PROBLEM DESCRIPTION
"""

editorial = """
# Editorial:
{}
"""

code = """
# Code:
{}
"""

def get_prompt(problem: Problem):
	assert problem.code is not None
	prompt = f'''
{task}
{requirement}
{answer_format}
{problem_statement.format(problem.name, problem.tags, problem.rating, problem.description)}
{editorial.format(problem.editorial)}
{code.format(problem.code)}
'''
	return helpers.remove_consecutive_line_breaks(prompt)

def parse(response):
	response = response.strip()
	if response.startswith('// START OF FORMAT'):
		response = response.split('// START OF FORMAT')[1].strip()
	if response.endswith('// END OF FORMAT'):
		response = response.split('// END OF FORMAT')[0].strip()
	if 'PROBLEM-UNDERSTANDING:' not in response:
		raise Exception('Invalid response format')
	if 'SOLUTION-REASONING:' not in response:
		raise Exception('Invalid response format')
	if 'IMPLEMENTATION-PLANNING:' not in response:
		raise Exception('Invalid response format')
	problem_understanding = response.split('PROBLEM-UNDERSTANDING:')[1].split('SOLUTION-REASONING:')[0].strip()
	for line in problem_understanding.split('\n'):
		# if line.lstrip().startswith('REASON:'):
			# raise Exception('Invalid response format')
		# if 'REASON:' not in line:
			# raise Exception('Invalid response format')
		if not line.lstrip().startswith('-'):
			raise Exception('Invalid response format')
	solution_reasoning = response.split('SOLUTION-REASONING:')[1].split('IMPLEMENTATION-PLANNING:')[0].strip()
	for line in solution_reasoning.split('\n'):
		# if line.lstrip().startswith('REASON:'):
			# raise Exception('Invalid response format')
		# if 'REASON:' not in line:
			# raise Exception('Invalid response format')
		if not line.lstrip().startswith('-'):
			raise Exception('Invalid response format')
	implementation_planning = response.split('IMPLEMENTATION-PLANNING:')[1].strip()
	return {
		'problem_understanding': problem_understanding,
		'solution_reasoning': solution_reasoning,
		'implementation_planning': implementation_planning
	}

def exists(name) -> bool:
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT name
	FROM summaries_v3
	WHERE name = %s
	""", (name,))
	exists = cursor.fetchone()
	cursor.close()
	return exists is not None

if __name__ == '__main__':
	model = Gemini()
	session_id = helpers.get_session_id()
	logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/checker.log', 'threadsafe': False})
	create_table_summary_v3()
	while True:
		problem_names = get_problem_names()
		print(len(problem_names))
		for name in problem_names:
			try:
				# if exists(name):
					# logger.info(f'Skipping: {name}')
					# continue
				problem = get_problem(name)
				print(problem.name)
				logger.info(f'Processing: {problem.name}')
				prompt = get_prompt(problem)
				response = model.generate_content(prompt)
				# print(response)
				summary = parse(response)
				logger.info(f'Generated: {problem.name}')
				insert_summary_v3(problem.name, response, summary['problem_understanding'], summary['solution_reasoning'], summary['implementation_planning'], session_id)
				logger.info(f'Inserted: {problem.name}')
			except Exception as e:
				logger.error(f'Error: {problem.name} - {e}')
				continue
			break