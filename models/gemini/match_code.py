import datasets
import psycopg2

from huggingface_hub import login
from model import Gemini
from constants import *
from datetime import datetime
from logger import get_logger

def get_db_conn():
    return psycopg2.connect(database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432'
)

def get_dataset_from_hf():
    login(HF_READ_TOKEN)
    dataset = datasets.load_dataset(EDITORIAL_DATASET, split='train', cache_dir='cache-editorial') 
    dataset = dataset.filter(lambda x: not x['has_code'])
    return dataset

def create_table_matches():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        reason TEXT NOT NULL,
        score INT NOT NULL,
        code TEXT NOT NULL,
        language TEXT NOT NULL,
        session_id TIMESTAMP
    )
    ''')
    conn.commit()
    cursor.close()

def insert_match(name, content, reason, score, code, language, session_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO matches (name, content, reason, score, code, language, session_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (name, content, reason, score, code, language, session_id))
    conn.commit()
    cursor.close()

def get_correct_solutions(contest_id, cf_index):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT solutions FROM problems WHERE cf_contest_id = {contest_id} AND cf_index = '{cf_index}';
    ''')
    problem = cursor.fetchone()
    cursor.close()
    solutions = problem[0]
    return solutions

# prompt template taken from Self-Rewarding Language Models - https://arxiv.org/pdf/2401.10020.pdf

def make_prompt_match(name, description, tags, editorial, code, language):
    return f"""You are an AI assistant in a competitive programming platform. You are given a problem's description, the problem's editorial, and a random correct solution crawled from the platform. Your task is to determine whether the code solution follows the editorial. That is the editorial is a detailed explanation on how to arrive at the code. And the code is a correct implementation of the editorial. You must give a reason behind your judgement and score the code solution based on the 5-point scoring system, starting with current point = 0:
- Add 1 point if the code is relevant and follows the general direction of the editorial. That is, both the code and the editorial are about the same topic (greedy, dynamic programming, graph, number theory, etc.). If so, write them out in the explanation.
- Add another point if the code follows the core idea of the editorial. That is, both the code and the editorial are about the same data structure/algorithm (Dijkstra, Kruskal, Segment Tree, etc.). If so, write them out in the explanation.
- Award a third point if there is a mathematical formula, case works, or step-by-step instruction in the editorial that is implemented in the code. If so, write them out in the explanation.
- Grant a fourth point if the code is a perfect match to the editorial. That is, the code can be splitted into sections that map to the sections in the editorial. If so, write them out in the explanation.
- Bestow a fifth point for a code that has meaningful NEW variable, function, class names, that is in the editorial. A name is considered NEW if the name is in the editorial but are not in the description. If so, write them out in the explanation.

# Here is the problem:
## Name: {name}
## Tags: {tags}
## Description:
{description}

# Here is the editorial:
{editorial}

# Here is the code:
```{language}
{code}
```

After examining the problem description, editorial, and code solution. Write a detailed review of the code solution based on the 5-point scoring system. Your answer must have 6 lines:
- The first 5 lines, each line for each point above: You must make a detailed judgement for and against whether to add the corresponding point to the current score. Finally, make a decision on adding a point or keeping the current score, write the current score.
- The 6-th line: Conclude with the final score in a single line using the exact format: “- My final score: <total points>”
"""

def good(content):
    if content.count('- My final score:') != 1:
        return False
    reason, score = content.split('My final score:')
    if reason.strip().strip('*') == '' or score.strip().strip('*') == '':
        return False
    if not score.strip().strip('*').isdigit():
        return False
    return True

def parse_content(content):
    reason, score = content.split('My final score:')
    return reason.strip().strip('*'), int(score.strip().strip('*'))

language_dict = ['', 'py', 'cpp', 'py', 'java']
favorite_lang = [4, 2, 0, 1, 3]

if __name__ == '__main__':
    model = Gemini(temperature=0, top_k=1, top_p=1)
    dataset = get_dataset_from_hf()
    print(dataset)
    create_table_matches()
    session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/match.log', 'threadsafe': False})
    for sample in dataset:
        solutions = get_correct_solutions(sample['contest'], sample['index'])
        logger.info(f'Generating content for problem {sample["name"]}')
        solutions = [(language, code) for (language, code) in zip(solutions['language'], solutions['solution'])]
        solutions = sorted(solutions, key=lambda x: favorite_lang[x[0]])
        for i, (language, code) in enumerate(solutions):
            logger.info(f'Generating content for problem {sample["name"]} with code {i}')
            prompt = make_prompt_match(sample['name'], sample['description'], sample['tags'], sample['editorial'], code, language_dict[language])
            try:
                content = model.generate_content(prompt)
                print(content)
                if not good(content):
                    raise Exception('Content is not good')
                reason, score = parse_content(content)
                insert_match(sample['name'], content, reason, score, code, language, session_id)
                if score == 5:
                    logger.info(f'Found perfect match for problem {sample["name"]}, code {i}')
                    break
                logger.info(f'Evaluated {sample["name"]}, code {i}, score = {score}')
            except Exception as e:
                logger.error(f'Error generating content for problem {sample["name"]}: {e}')


