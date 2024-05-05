import datasets
import unicodedata

from datetime import datetime
from huggingface_hub import login
from model import Gemini
from constants import *
from match_code import get_db_conn
from logger import get_logger

def get_dataset_from_hf():
	login(HF_READ_TOKEN)
	dataset = datasets.load_dataset(EDITORIAL_DATASET, split='train', cache_dir='cache-editorial')	
	return dataset

def create_table_categories():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS categories (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255),
		content TEXT,
		session_id VARCHAR(255)
	)
	''')
	conn.commit()
	cursor.close()

def insert_categories(name, content, session_id):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	INSERT INTO categories (name, content, session_id)
	VALUES (%s, %s, %s)
	''', (name, content, session_id))
	conn.commit()
	cursor.close()

single_code_prompt = """# Task
You are an AI assistant for an editorialist of a competitive programming website.
You are given a problem's statement, the problem's editorial on how to solve the problem.
Your task is to extract out, categorize, and re-structure all the main points in the editorial.

# What to do:
Split the editorial into multiple short, disjointed, and continuous sections (a section is a sentence, a group of sentences, a paragraph, etc.).
Categorize that section into one of the following categories:
- A section is a PREMISE if the section introduce a new definition, concept that is necessary to solve the problem. (For example, "let dp[i] be the maximum sum of subarray ending at index i" is a PREMISE, "let x be the number of apples" is a PREMISE)
- A section is an OBSERVATION if the section is a fact, observation, or a conclusion. (For example, "the maximum sum of subarray ending at index i is the maximum of dp[i-1] + a[i] and a[i]" is an OBSERVATION)
- A section is a FACT if the section mentions a common mathematical principle, a common knowledge, or a common sense. (For example, "the maximum of two numbers is the maximum of the first number and the second number" is a FACT)
- A section is a STRATEGY if the section mentions a strategy, a plan, a method, or a technique. (For example, "we can use dynamic programming to solve this problem" is a STRATEGY, "we can use segment tree to calculate the sum of subarray" is a STRATEGY)
- A section is a MATH-WORK if the section involves lengthy mathematical calculations, derivations, or proofs that is true specifically for this problem and not a common knowledge. (For example, "$a = t^2 + 2t + 1 \iff a = (t + 1)^2 \implies \sqrt a = t + 1 \iff t = 1 - \sqrt a$" is a MATH-WORK)
- A section is a CASE-WORK if the section involves lengthy case analysis, or a proof by cases. (For example, "if a is even, we can divide a by 2, otherwise, we can subtract 1 from a" is a CASE-WORK)
- A section is a EXAMPLE if the section provides an example, a counter-example, or a test case. (For example, "for example, if a = 5, the maximum sum of subarray ending at index 2 is 5" is an EXAMPLE)
- A section is a COMMENT if the section is just the editorialist's comment, opinion, or a side note without any relevant information to solve the problem. (For example, "this problem is very interesting" is a COMMENT, "this problem can also be solved by dynamic programming, but we are not discussing it here." is a COMMENT)
- A section is a CODE if the section is a code snippet, a code block, or a code explanation. (For example, "```cpp\nint dp[100];\n```" is a CODE)
- A section is a UNCLASSIFIED if the section does not belong to any of the above categories.

# Each section MUST be in the following format:
**CONTENT**
{{quote EXACTLY a section from the editorial}}
**REASONING**
{{reason about the properties of the section to decide which category it belongs to}}
**CONCLUSION**
{{exactly one of these categories: PREMISE, OBSERVATION, FACT, STRATEGY, MATH-WORK, CASE-WORK, EXAMPLE, COMMENT, CODE, UNCLASSIFIED}}
**CONTENT**
{{quote EXACTLY a section from the editorial}}
**REASONING**
{{reason about the properties of the section to decide which category it belongs to}}
**CONCLUSION**
{{exactly one of these categories: PREMISE, OBSERVATION, FACT, STRATEGY, MATH-WORK, CASE-WORK, EXAMPLE, COMMENT, CODE, UNCLASSIFIED}}
... (repeat for all sections)

# Here is the problem statement:
{}

# Here is the editorial:
{}
"""

def make_prompt(name, description, tags, editorial): 
	return single_code_prompt.format(f"Name: {name}\nTags: {', '.join(tags)}\n{description}", editorial)

def remove_double_newline(text):
	while '\n\n' in text:
		text = text.replace('\n\n', '\n')
	return text

def good(summary, editorial):
	sections = summary.split('**CONTENT**')[1:]
	editorial = unicodedata.normalize('NFKD', editorial)
	editorial = ''.join(editorial.split()).replace(',', '')
	sections = [section.strip() for section in sections if section.strip() != '' and section.strip() != '```']
	for section in sections:
		section_content = section.split('**REASONING**')[0].strip()
		section_content = unicodedata.normalize('NFKD', section_content)
		tmp = ''.join(section_content.split()).replace(',', '')
		if tmp not in editorial:
			return False, f'Section content "{section_content}" not in editorial'
		category = section.split('**CONCLUSION**')[1].strip()
		if category not in ['PREMISE', 'OBSERVATION', 'FACT', 'STRATEGY', 'MATH-WORK', 'CASE-WORK', 'EXAMPLE', 'COMMENT', 'CODE', 'UNCLASSIFIED']:
			return False, f'Category conclusion "{category}" is not valid'
	return True, 'All sections are valid'

def generate_content(model, prompt, name, editorial, session_id, logger):
	try:
		summary = model.generate_content(prompt)
		is_good, reason = good(summary, editorial)
		if not is_good:
			raise Exception(f'{reason}\nsummary:\n{summary}')
		insert_categories(name, summary, session_id)
	except Exception as e:
		logger.error(f'Error generating content for problem {name}: {e}')
		if e.args[0].startswith('LLM.generate_content error:'):
			return True
		return False
	return True

start_time = datetime.now()
end_time = datetime.now()

def redo(name):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM categories WHERE name = %s', (name,))
	result = cursor.fetchone()
	cursor.close()
	if result is None:
		return True
	# content = result[2]
	# if '```' in content and ('\nCODE\n' not in content or content.endswith('\nCODE')):
	#	return True
	return False

if __name__ == '__main__':
	model = Gemini(temperature=0.8, top_k=50, top_p=1)
	dataset = get_dataset_from_hf()
	create_table_categories()
	session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/categorize.log', 'threadsafe': False})
	start_doing = False
	for problem in dataset:
		contest = problem['contest']
		index = problem['index']
		name = problem['name']
		if not redo(name):
			continue
		description = problem['description']
		tags = problem['tags']
		editorial = problem['editorial'].split('# TUTORIAL CODE XXX')[0].strip().replace(' (REFERENCE)**', '**')
		description = remove_double_newline(description)
		editorial = remove_double_newline(editorial)
		prompt = make_prompt(name, description, tags, editorial)
		logger.info(f'Generating content for problem {name}')
		retry = 10
		while retry > 0:
			end_time = datetime.now()
			duration_in_s = (end_time - start_time).total_seconds()
			if duration_in_s < 1:
				continue
			start_time = end_time
			print(f'Generating content for {name} retry {10 - retry + 1}/10')
			if generate_content(model, prompt, name, editorial, session_id, logger):
				break
			retry -= 1
		else:
			logger.error(f'Failed to generate content for problem {name}')

		
