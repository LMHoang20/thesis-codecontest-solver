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
output_dir = 'data/contests-v2'
os.makedirs(output_dir, exist_ok=True)

with open(CLEAN_EDITORIAL_CONTENT_PATH, 'r') as editorial_file:
    for line in editorial_file:
        editorial_data = json.loads(line)
        contest_id = editorial_url_to_contest[editorial_data['url']]
        if contest_id in done:
            continue
        done.add(contest_id)
        problems = contest[contest_id]
        contest_id = str(contest_id)
        editoiral_url = editorial_data['url']
        contest_dir = os.path.join(output_dir, contest_id)
        os.makedirs(contest_dir, exist_ok=True)
        with open(os.path.join(contest_dir, 'editorial.md'), 'w') as f:
            f.write(f"# Editorial for contest {contest_id}\n\n")
            f.write(f"Editorial url: {editoiral_url}\n\n")
            for problem in problems:
                if problem['url'] in problem_to_editorial_url:
                    f.write(f"- [{problem['cf_index']}. {problem['name']}]({problem['url']})\n")
                else:
                    f.write(f"- {problem['cf_index']}. {problem['name']}\n")
            f.write(editorial_data['content'])

print(len(done))
