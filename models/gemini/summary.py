import datasets
import os
import time

from huggingface_hub import login
from inference import get_db_conn
from model import Gemini
from constants import *

def create_table_small_summary():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS small_summaries (
		id SERIAL PRIMARY KEY,
		name TEXT NOT NULL,
		content TEXT NOT NULL
	)
	''')
	conn.commit()
	cursor.close()

def insert_small_summary(name, content):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	INSERT INTO small_summaries (name, content)
	VALUES (%s, %s)
	""", (name, content))
	conn.commit()
	cursor.close()

def make_prompt(name, description, tags, editorial, code, multiple_code = False): 
	parts = "- Write a summary consists of 2 parts: observation and planning."
	meta_reasoning = ""
	note = ""
	start_tag = "<OBSERVATION>"
	if multiple_code:
		parts = """
- Write a summary consists of 3 parts: meta-reasoning, observation and planning."""
		meta_reasoning = """
- Meta-reasoning part is to reason which solution the code belongs to based on the comment in the first line of the code.
- Meta-reasoning must be wrapped in <META-REASONING> and </META-REASONING> tags."""
		note = """# Note:
- The editorial have multiple solutions.
- Use the comment in the first line of the code to determine the correct solution for the summary.
- Extract and explain ONLY the solution corresponding to the code implementation.
"""
		start_tag = "<META-REASONING>"
	task = f"""<TASK>
# Context:
- You are a student interested in competitive programming.
- You want write a summary of the editorial of a problem to understand the problem better.
- You are given a problem, its original editorial, and a code solution.
- Your task is to summarize the editorial of the problem and the code implementation.
# What to do:{parts}{meta_reasoning}
- Observation part is to extract out the observations, conclusions, insights, edge cases and reasoning from the editorial and the code. Focus on the editorial part.
- Observation must be wrapped in <OBSERVATION> and </OBSERVATION> tags.
- Planning part is to list out step by steps, following the flow of the code, starting from the main function, to understand the code implementation.
- Planning must be wrapped in <PLANNING> and </PLANNING> tags.
- The length of the summary must be long and detailed, 10 to 20 bullet points for each of the observation and planning part.
{note}</TASK>
"""
	return task + f"""<PROBLEM>
# Problem information:
- Name: {name}
- Tags: {tags}
# Problem description:
{description}
</PROBLEM>
<EDITORIAL>
{editorial}
</EDITORIAL>
<CODE>
{code}
</CODE>
{start_tag}
"""


if __name__ == '__main__':
	model = Gemini()
	dataset = get_dataset_from_hf()
	create_table_summary()
	for problem in dataset:
		contest = problem['contest']
		index = problem['index']
		name = problem['name']
		description = problem['description']
		tags = problem['tags']
		editorial = problem['editorial']
		sections = editorial.split('# TUTORIAL CODE XXX')
		print(f"Start: {contest} {index}")
		while '\n\n' in description:
			description = description.replace('\n\n', '\n')
		try:
			assert len(sections) > 1, f"Problem {name} has no code"
		except Exception as e:
			continue
		editorial = sections[0].strip().replace(' (REFERENCE)**', '**')
		while '\n\n' in editorial:
			editorial = editorial.replace('\n\n', '\n')
		for i in range(1, len(sections)):
			print(f"Processing: {contest} {index} {i}")
			code = sections[i].strip()
			prompt = make_prompt(name, description, tags, editorial, code, len(sections) > 2)
			try:
				response = model.generate_content(prompt)
				summary = response.text
				insert_summary(contest, index, summary)
			except Exception as e:
				continue
		print(f"Done: {contest} {index}")
