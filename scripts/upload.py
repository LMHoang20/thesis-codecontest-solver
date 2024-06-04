import huggingface_hub
import datasets
import subprocess
import sys

from constants import *
from database import get_db_conn

def load_problem_with_editorial():
	conn = get_db_conn()
	cur = conn.cursor()
	cur.execute("""
		SELECT cf_contest_id, cf_index, name, description, cf_tags, editorial
		FROM problems
		WHERE editorial != ''
		ORDER BY cf_contest_id, cf_index
	""")
	data = cur.fetchall()
	return data

def get_all_links():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	SELECT * FROM links
	''')
	rows = cursor.fetchall()
	cursor.close()
	
	return dict([
	(f'[{row[3]}]({row[0]})', (row[3], row[4], row[5])) for row in rows
	])

def replace_link_to_code(linkToCode, editorial):
	for link in linkToCode:
		if link in editorial:
			placeholder, code, language = linkToCode[link]
			editorial = editorial.replace(link, f"""
# TUTORIAL CODE XXX
```{language}
// Note: {placeholder}
{code}
```
""")
	return editorial


language_dict = {
    "FPC": "pascal",
    "GNU C++17": "cpp",
    "C++17 (GCC 9-64)": "cpp", 
    "Python 3": "py",
    "GNU C++14": "cpp",
    "GNU C++0x": "cpp",
    "python": "py",
    "GNU C++": "cpp",
    "PyPy 2": "py",
    "GNU C++11": "cpp",
    "Java 6": "java",
    "Java 8": "java",
    "GNU C11": "c",
    "java": "java",
    "C++14 (GCC 6-32)": "cpp",
    "GNU C++17 (64)": "cpp",
    "Python 2": "py",
    "text": "cpp",
    "MS C++": "cpp",
    "C++17 (GCC 7-32)": "cpp",
    "PyPy 3": "py",
    "C++20 (GCC 11-64)": "cpp",
    "Java 7": "java",
    "cpp": "cpp",
    "Kotlin 1.4": "kotlin",
}

def create_dataset(data):
	dataset = {
		'contest': [],
		'index': [],
		'name': [],
		'description': [],
		'tags': [],
		'editorial': [],
		'has_code': []
	}
	linkToCode = get_all_links()
	startDoing = True
	for row in data:
		contest, index, name, description, tags, editorial = row
		if contest == int(sys.argv[1]) and index == sys.argv[2]:
			startDoing = True
		if contest == 1325 and index == 'F':
			continue
		if contest == 1028 and index == 'H':
			continue
		if contest == 1060 and index == 'H':
			continue
		if contest == 1167 and index == 'G':
			continue
		if contest == 1261 and index == 'B2':
			continue
		if contest == 1361 and index == 'F':
			continue
		if contest == 1383 and index == 'F':
			continue
		if not startDoing:
			continue
		print(contest, index)
		editorial = editorial[editorial.find('\n') + 1:].strip()
		editorial = replace_link_to_code(linkToCode, editorial)
		has_code = '# TUTORIAL CODE XXX' in editorial
		if has_code:
			sections = editorial.split('# TUTORIAL CODE XXX')
			solution = sections[0].strip()
			editorial = solution
			for code in sections[1:]:
				code = code.strip()
				for language in language_dict:
					if f'```{language}\n' in code:
						code = code.replace(f'```{language}', f'```{language_dict[language]}')
				if '```cpp' in code:
					code_content = code.split(f'```cpp')[1]
					code_content = code_content.split('```')[0]
					with open('tmp.cpp', 'w') as f:
						f.write(code_content)
					command = 'python normalize_code.py tmp.cpp'
					try:
						subprocess.run(command, shell=True, check=True)
					except subprocess.CalledProcessError as e:
						print(contest, index, e)
						exit(0)
					with open('tmp.cpp', 'r') as f:
						code_content = f.read().strip()
					compile_result = subprocess.run(["g++", "--std=c++20", "-w", "-fsyntax-only", "-I", "/Users/hoangle/Other/thesis/thesis-codecontest-solver", "tmp.cpp"], capture_output=True, text=True)
					if compile_result.stderr:
						compile_result = subprocess.run(["g++", "--std=c++14", "-w", "-fsyntax-only", "-I", "/Users/hoangle/Other/thesis/thesis-codecontest-solver", "tmp.cpp"], capture_output=True, text=True)
						if compile_result.stderr:
							print(editorial, compile_result.stderr, contest, index)
							exit(0)
					code = f'```cpp\n{code_content}\n```'
				editorial += f"\n# TUTORIAL CODE XXX\n{code}"
		dataset['contest'].append(row[0])
		dataset['index'].append(row[1])
		dataset['name'].append(row[2])
		dataset['description'].append(row[3])
		dataset['tags'].append(row[4])
		dataset['editorial'].append(editorial)
		dataset['has_code'].append(has_code)
	return datasets.Dataset.from_dict(dataset)
		
def upload_dataset_to_hf(dataset, dataset_name):
	huggingface_hub.login(HF_WRITE_TOKEN)
	dataset.push_to_hub(dataset_name)

if __name__ == "__main__":
	huggingface_hub.login(HF_WRITE_TOKEN)

	data = load_problem_with_editorial()

	dataset_name = EDITORIAL_DATASET

	dataset = create_dataset(data)

	upload_dataset_to_hf(dataset, dataset_name)
