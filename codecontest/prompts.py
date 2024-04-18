import json
import os
import shutil

from constants import *

contest = dict()

with open(PROBLEM_URLS_PATH, 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['cf_contest_id'] not in contest:
            contest[data['cf_contest_id']] = []
        contest[data['cf_contest_id']].append(data)

for contest_id, problems in contest.items():
    contest[contest_id] = sorted(problems, key=lambda x: x['cf_index'])

problem_to_editorial_url = dict()
editorial_to_problem_url = dict()
editorial_url_to_contest = dict()

with open(CLEAN_EDITORIAL_URLS_PATH, 'r') as f:
    for line in f:
        data = json.loads(line)
        problem_to_editorial_url[data['url']] = data['editorial_url']
        editorial_to_problem_url[data['editorial_url']] = data['url']

for contest_id, problems in contest.items():
    for problem in problems:
        if problem['url'] in problem_to_editorial_url:
            editorial_url_to_contest[problem_to_editorial_url[
                problem['url']]] = contest_id
            break

done = set()

os.makedirs('data/prompts', exist_ok=True)
with open(CLEAN_EDITORIAL_CONTENT_PATH, 'r') as editorial_file:
    for line in editorial_file:
        editorial_data = json.loads(line)
        contest_id = editorial_url_to_contest[editorial_data['url']]
        if contest_id in done:
            continue
        done.add(contest_id)
        problems = contest[contest_id]
        contest_id = str(contest_id)
        editorial_url = editorial_data['url']
        editorial = editorial_data['content'].strip()
        while '\n\n\n' in editorial:
            editorial = editorial.replace('\n\n\n', '\n\n')
        os.makedirs(f'data/prompts/{contest_id}', exist_ok=True)
        for problem in problems:
            id = f'{contest_id}_{problem["cf_index"]}. '
            name = problem['name'][problem['name'].find(id) + len(id):]
            print(name)
            with open(f'data/prompts/{contest_id}/{problem["cf_index"]}-prompt.md', 'w') as f:
                f.write("<TARGET>\n")
                f.write(f'problem name: {name}\n')
                f.write("</TARGET>\n")
                f.write("<EDITORIAL>\n")
                f.write(editorial)
                f.write("\n</EDITORIAL>\n")
