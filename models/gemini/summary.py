import datasets
import os
from huggingface_hub import login
from inference import get_db_conn
from model import Gemini
from constants import *

def get_dataset_from_hf():
	login(HF_READ_TOKEN)
	dataset = datasets.load_dataset(EDITORIAL_DATASET, split='train', cache_dir='cache-editorial') 
	dataset = dataset.filter(lambda x: x['has_code'])
	return dataset

def create_table_summary():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS summaries (
		id SERIAL PRIMARY KEY,
		contest_id VARCHAR(10) NOT NULL,
		problem_id VARCHAR(10) NOT NULL,
		summary TEXT NOT NULL
	)
	''')
	conn.commit()
	cursor.close()

def insert_summary(contest, problem_id, summary):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO summaries (contest_id, problem_id, summary)
		VALUES (%s, %s, %s)
	''', (contest, problem_id, summary))
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
- The length of the summary must be 10 to 20 bullet points for each of the observation and planning part.
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
	with open('log-summary.txt', 'w') as log:
		for problem in dataset:
			contest = problem['contest']
			index = problem['index']
			name = problem['name']
			description = problem['description']
			tags = problem['tags']
			editorial = problem['editorial']
			sections = editorial.split('# TUTORIAL CODE XXX')
			print(f"Start: {contest} {index}")
			log.write(f"Start: {contest} {index}\n")
			while '\n\n' in description:
				description = description.replace('\n\n', '\n')
			try:
				assert len(sections) > 1, f"Problem {name} has no code"
			except Exception as e:
				log.write(f"Error: {contest} {index}: {e}\n")
				continue
			editorial = sections[0].strip().replace(' (REFERENCE)**', '**')
			while '\n\n' in editorial:
				editorial = editorial.replace('\n\n', '\n')
			for i in range(1, len(sections)):
				print(f"Processing: {contest} {index} {i}")
				log.write(f"Processing: {contest} {index} {i}\n")
				code = sections[i].strip()
				prompt = make_prompt(name, description, tags, editorial, code, len(sections) > 2)
				try:
					response = model.generate_content(prompt)
					summary = response.text
					insert_summary(contest, index, summary)
				except Exception as e:
					log.write(f"Error: {contest} {index} {i}: {e}\n")
					continue
			print(f"Done: {contest} {index}")
			log.write(f"Done: {contest} {index}\n")
			log.flush()