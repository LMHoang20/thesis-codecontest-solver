import pathlib
import google.generativeai as genai
import psycopg2

from constants import *

def get_model():
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    genai.configure(api_key=GOOGLE_API_KEY)

    return genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)

def few_shot_prompting():
        task = ''
        with open(pathlib.Path('models/gemini/task.md'), 'r') as file:
            task = file.read()
        result = ''
        for i in range(1, 5):
            with open(pathlib.Path(f'models/gemini/prompt-{i}.md'), 'r') as file:
                prompt = file.read()
                result += task + '\n\n' + prompt + '\n'
        return result + task

def get_db_conn():
    return psycopg2.connect(database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432'
)

def select_problem_name_description(dbconn, contest_id, cf_index):
    cursor = dbconn.cursor()
    cursor.execute(f'''
    SELECT name, description FROM problems WHERE cf_contest_id = {contest_id} AND cf_index = '{cf_index}';
    ''')
    problem = cursor.fetchone()
    cursor.close()
    name, description = problem
    return name, description

def select_problem_public_tests(dbconn, contest_id, cf_index):
    cursor = dbconn.cursor()
    cursor.execute(f'''
    SELECT public_tests FROM problems WHERE cf_contest_id = {contest_id} AND cf_index = '{cf_index}';
    ''')
    problem = cursor.fetchone()
    cursor.close()
    tests = problem[0]
    return [(test_input, test_output) for test_input, test_output in zip(tests['input'], tests['output'])]
    
def get_prompt(few_shot, dbconn, contest_id, cf_index, editorial, code):
    name, description = select_problem_name_description(dbconn, contest_id, cf_index)
    return f'''
{few_shot}

## Name

{name}

## Description

{description}

## Editorial

{editorial}

## Code

```cpp
{code}
```
'''

def get_next_answer_prompt():
    return """
# Answer

Correct code:
"""

def compile_error_prompt(code, message):
    return f"""# Answer
                                                                
Incorrect code:
{code}

# Compiler Output
{message}
"""

def main():
    few_shot = few_shot_prompting()
    dbconn = get_db_conn()
    model = get_model()
    done = set()
    with open('done.txt', 'r') as f:
        done = set(f.read().split('\n'))
    start_doing = False
    for _, dirs, _ in os.walk('data/contests'):
        for dir in dirs:
            if '-done' not in dir:
                continue
            contest_id = dir.split('-')[0]
            for _, _, files in os.walk(f'data/contests/{dir}'):
                for file in files:
                    if '-' in file:
                        continue
                    if 'editorial' in file:
                        continue
                    if f'{contest_id}-{file.split(".")[0]}' in done:
                        continue
                    if contest_id == '1290' and file.split('.')[0] == 'F':
                        start_doing = True
                    if not start_doing:
                        continue
                    with open(f'data/contests/{dir}/{file}', 'r') as f:
                        content = f.read()
                        content = content.split('\n', 1)[1]
                    split = content.split('# TUTORIAL CODE XXX')
                    editorial = split[0].strip()
                    solutions = split[1:]
                    index = file.split('.')[0]
                    if contest_id == '1519' and index == 'F':
                        continue
                    public_tests = select_problem_public_tests(dbconn, contest_id, index)
                    print(contest_id, index)
                    for i, solution in enumerate(solutions):
                        if '```cpp' not in solution:
                            continue
                        note = solution.split('```')[0].strip()
                        code = solution.split('```cpp')[1]
                        code = code.split('```')[0]
                        code = code.strip()
                        if note != '':
                            code = f'/*\n{note}\n*/\n{code}'
                        prompt = get_prompt(few_shot, dbconn, contest_id, index, editorial, code)
                        for meow in range(3):
                            with open(f'prompt-{meow}.md', 'w') as trace:
                                trace.write(prompt + get_next_answer_prompt())
                            response = model.generate_content(prompt + get_next_answer_prompt()) 
                            response_code = response.text.split('```cpp')[1]
                            response_code = response_code.split('```')[0]
                            compiled, message = (False, '')
                            if not compiled and len(message) < 100:
                                prompt += compile_error_prompt(response_code, message)
                                print(message)
                            elif message != 'OK':
                                prompt = get_prompt(few_shot, dbconn, contest_id, index, editorial, code)
                            else:
                                with open(f'data/contests/{dir}/{index}-{i}-refactored.cpp', 'w') as f:
                                    f.write(response_code)
                                with open('done.txt', 'a') as f:
                                    f.write(f'{contest_id}-{index}-{i}\n')
                                break
                        else:
                            with open('refactor-failed.txt', 'a') as f:
                                f.write(f'{contest_id}-{index}-{i}\n')
    

if __name__ == '__main__':
    main()