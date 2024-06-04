from helpers import get_session_id
from models import get_llm_model
from logger import get_logger
from database import get_db_conn

from random import shuffle

import yaml

def create_table_matches_v2():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches_v2 (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        score INT NOT NULL,
        code TEXT NOT NULL,
        language TEXT NOT NULL,
        session_id TIMESTAMP
    )
    """)
    conn.commit()
    cur.close()

def insert_match_v2(name, content, score, code, language, session_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO matches_v2 (name, content, score, code, language, session_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, content, score, code, language, session_id))
    conn.commit()
    cur.close()

def check_exists(name):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT name
    FROM matches_v2
    WHERE name = %s
    AND score = 5
    """, (name,))
    return cur.fetchone() is not None

def get_problem_names():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.name, p.cf_contest_id, p.cf_index
    FROM problems p JOIN editorials e ON p.name = e.name
    """)
    return cur.fetchall()

def get_name(cf_contest_id, cf_index, test=False):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT name
    FROM {f'testing_problems' if test else 'problems'}
    WHERE cf_contest_id = %s
    AND cf_index = %s
    """, (cf_contest_id, cf_index))
    if cur.rowcount == 0:
        print("CANT FIND", cf_contest_id, cf_index)
        return None
    return cur.fetchone()[0]

editorial_dict = {}
def get_extra_problem_names():
    import os
    result = []
    for root, dirs, files in os.walk('data/contests-extra'):
        for dir in dirs:
            if 'skip' in dir:
                continue
            if 'generated' not in dir:
                continue
            for root, _, files in os.walk(f'data/contests-extra/{dir}'):
                for file in files:
                    if 'skip' in file:
                        continue
                    if 'editorial' in file:
                        continue
                    if 'corrected' not in file:
                        continue
                    with open(f'{root}/{file}', 'r') as f:
                        lines = f.readlines()
                        lines = lines[1:]
                        lines = list(filter(lambda x: x.strip() != '', lines))
                        content = ''.join(lines)
                        if 'TUTORIAL CODE XXX' in content:
                            continue
                    contest_id = dir.split('_')[0].split('-')[0]
                    index = file.split('.')[0].split('-')[0]
                    name = get_name(contest_id, index)
                    if name is not None:
                        result.append((name, contest_id, index))
                        editorial_dict[name] = content
    return result

def get_extra_problem_names_2():
    import os
    result = []
    for root, dirs, files in os.walk('data/contests-extra'):
        for dir in dirs:
            if 'skip' in dir:
                continue
            if 'generated' in dir:
                continue
            for root, _, files in os.walk(f'data/contests-extra/{dir}'):
                for file in files:
                    if 'skip' in file:
                        continue
                    if 'editorial' in file:
                        continue
                    with open(f'{root}/{file}', 'r') as f:
                        lines = f.readlines()
                        lines = lines[1:]
                        lines = list(filter(lambda x: x.strip() != '', lines))
                        content = ''.join(lines)
                        if '# TUTORIAL CODE XXX' in content:
                            continue
                    contest_id = dir.split('_')[0].split('-')[0]
                    index = file.split('.')[0].split('-')[0]
                    name = get_name(contest_id, index)
                    if name is not None:
                        result.append((name, contest_id, index))
                        editorial_dict[name] = content
    return result

def get_validate_problem_names():
    import os
    result = []
    for root, dirs, _ in os.walk('data/validate_set'):
        for dir in dirs:
            for root, _, files in os.walk(f'data/validate_set/{dir}'):
                for file in files:
                    if 'skip' in file:
                        continue
                    if 'editorial' in file:
                        continue
                    with open(f'{root}/{file}', 'r') as f:
                        lines = f.readlines()
                        lines = lines[1:]
                        lines = list(filter(lambda x: x.strip() != '', lines))
                        content = ''.join(lines)
                        if '# TUTORIAL CODE XXX' in content:
                            continue
                    contest_id = dir.split('_')[0].split('-')[0]
                    index = file.split('.')[0].split('-')[0]
                    name = get_name(contest_id, index, test=True)
                    if name is not None:
                        result.append((name, contest_id, index))
                        editorial_dict[name] = content
    return result

def get_problem_description(name, test=False):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT description
    FROM {f'testing_problems' if test else 'problems'}
    WHERE name = %s
    """, (name,))
    return cur.fetchone()[0]

def get_editorial_solution(name):
    if name in editorial_dict:
        return editorial_dict[name], []
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT content, solutions
    FROM editorials
    WHERE name = %s
    """, (name,))
    return cur.fetchone()

def get_correct_solutions(name, test=False):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT solutions
    FROM {f'testing_problems' if test else 'problems'}
    WHERE name = %s
    """, (name,))
    return cur.fetchone()[0]

def score_code(model, description, editorial, language, code):
    system_prompt = """# System:
You are an AI assistant in a competitive programming platform. You are given a problem's description, the problem's editorial, and a random correct solution crawled from the platform. Your task is to determine whether the code solution follows the editorial. That is the editorial is a detailed explanation on how to arrive at the code. And the code is a correct implementation of the editorial. You must give a reason behind your judgement and score the code solution based on the 5-point scoring system, starting with current point = 0:
- Relevancy: Add 1 point if the code is relevant and follows the general direction of the editorial. That is, both the code and the editorial are about the same topic (greedy, dynamic programming, graph, number theory, etc.). If so, write them out in the explanation.
- Core: Add another point if the code follows the core idea of the editorial. That is, both the code and the editorial are about the same data structure/algorithm (Dijkstra, Kruskal, Segment Tree, etc.). If so, write them out in the explanation.
- Detail: Award a third point if there is a mathematical formula, case works, or step-by-step instruction in the editorial that is implemented in the code. If so, write them out in the explanation.
- Perfect: Grant a fourth point if the code is a perfect match to the editorial. That is, the code can be splitted into sections that map to the sections in the editorial. If so, write them out in the explanation.
- Readability: Bestow a fifth point for a code that is readable and easy to understand.
"""
    formatting = """# Formatting:
You must answer in yaml format with this exact structure:
```yaml
---
points:
  - name: Relevancy
    editorial: |
        <extracted section of the editorial>
    code: |
        <extracted section of the code>
    reasoning: |
        <analyze if the code is relevant and follows the general direction of the editorial>
    add point: YES/NO
  - name: Core
  	editorial: |
        <extracted section of the editorial>
    code: |
        <extracted section of the code>
    reasoning: |
        <analyze if the code follows the core idea of the editorial>
    add point: YES/NO
  - name: Detail
    editorial: |
        <extracted section of the editorial>
    code: |
        <extracted section of the code>
    reasoning: |
        <analyze if the code has a mathematical formula, case works, or step-by-step instruction in the editorial>
    add point: YES/NO
  - name: Perfect
    reasoning: |
        <analyze if the code is a perfect match to the editorial>
    add point: YES/NO
  - name: Readability
    reasoning: |
        <analyze if the code is readable and easy to understand>
    add point: YES/NO
``` 
"""
    problem_statement = f"""# Problem:
{description}
# Editorial:
{editorial}
# Code:
```{language}
{code}
```
"""
    start_prompt = """```yaml
---
points:
  - name: """
    prompts = [system_prompt, formatting, problem_statement, start_prompt]
    result = model.generate(prompts).strip()
    if start_prompt not in result:
        result = start_prompt + result
    if result.startswith('```yaml'):
        result = result[8:]
    if result.endswith('```'):
        result = result[:-3]
    return result

language_dict = ['', 'py', 'cpp', 'py', 'java']

def match_code(name, cf_contest_id, cf_index, model, session_id, logger):
    print(name)
    if check_exists(name):
        return
    if name.startswith('409_') or name.startswith('391_'):
        return
    if name in ['610_C. Harmony Analysis', '406_C. Graph Cutting', '98_E. Help Shrek and Donkey']:
        # id = name.split('.')[0]
        # with open(f'{id}.cpp', 'r') as f:
        #     code = f.read()
        # insert_match_v2(name, 'human labeled', 5, code, 'cpp', session_id)
        return
    description = get_problem_description(name, test=True)
    editorial, solutions = get_editorial_solution(name)
    if len(solutions) > 0:
        return
    logger.info(f"Matching code for {name} ({cf_contest_id}/{cf_index})")
    solutions = get_correct_solutions(name, test=True)
    solutions = [(code, language) for code, language in zip(solutions['solution'], solutions['language'])]
    solutions = list(filter(lambda x: x[1] == 1 or x[1] == 2 or x[1] == 3, solutions))
    if len(solutions) == 0:
        logger.error(f"No correct solutions found for {name} ({cf_contest_id}/{cf_index})")
        return
    shuffle(solutions)
    # if len(solutions) > 5:
    #     solutions = solutions[:5]
    for index, (code, language) in enumerate(solutions):
        try:
            logger.info(f"Matching code for {name} ({cf_contest_id}/{cf_index}) with code {index}/{len(solutions)}")
            language = language_dict[language]
            result = score_code(model, description, editorial, language, code)
            score = yaml.safe_load(result)
            score = sum([1 for point in score['points'] if point['add point']])
            insert_match_v2(name, result, score, code, language, session_id)
            if score == 5:
                logger.info(f"Found perfect match for {name} ({cf_contest_id}/{cf_index})")
                break
        except Exception as e:
            logger.error(e)

def main():
    # problems = get_problem_names()
    # problems = get_extra_problem_names_2()
    problems = get_validate_problem_names()
    problems = list(problems)
    session_id = get_session_id()
    model = get_llm_model('gemini')
    logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/match-v2-extra.log', 'threadsafe': False})
    create_table_matches_v2()
    for name, cf_contest_id, cf_index in problems:
        match_code(name, cf_contest_id, cf_index, model, session_id, logger)
        

if __name__ == '__main__':
    main()