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

os.makedirs('data/tmp-contests', exist_ok=True)

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
        sus = ""
        for dir in os.listdir('data/contests'):
            if dir.startswith(f"{contest_id}-"):
                sus = dir
                break
        if sus == "":
            with open(
                    os.path.join('data/contests', contest_id, 'editorial.md'),
                    'w') as f:
                f.write(
                    f'Editorial URL: [{editoiral_url}]({editoiral_url})\n\n')
                for problem in problems:
                    f.write(
                        f'\n\n## [{problem["cf_index"]}. {problem["name"]}]({problem["url"]})\n\n'
                    )
                    # with open(os.path.join('data/contests', contest_id, problem['cf_index'] + '.md'), 'w') as f2:
                    # f2.write(f'# {problem["cf_index"]}: {problem["name"]}\n\n')
                f.write(editorial_data['content'])
        else:
            if os.path.exists(os.path.join('data/contests', contest_id)):
                shutil.move(os.path.join('data/contests', contest_id),
                            os.path.join('data/tmp-contests', contest_id))
            with open(os.path.join('data/contests', sus, 'editorial.md'),
                      'w') as f:
                f.write(
                    f'Editorial URL: [{editoiral_url}]({editoiral_url})\n\n')
                for problem in problems:
                    f.write(
                        f'\n\n## [{problem["cf_index"]}. {problem["name"]}]({problem["url"]})\n\n'
                    )
                    # with open(os.path.join('data/contests', contest_id, problem['cf_index'] + '.md'), 'w') as f2:
                    # f2.write(f'# {problem["cf_index"]}: {problem["name"]}\n\n')
                f.write(editorial_data['content'])

print(len(done))
