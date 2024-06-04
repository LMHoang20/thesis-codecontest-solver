import os
from download_code import get_db_conn

def insert_db(contest_id, problem_id, editorial):
    if editorial[editorial.find('\n') + 1:].strip() == '':
        return 'failed'
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE problems SET editorial = %s WHERE cf_contest_id = %s AND cf_index = %s
    ''', (editorial, contest_id, problem_id))
    conn.commit()
    cursor.close()
    return 'success'

cnt = set()

for root, dirs, _ in os.walk('data/contests'):
    for dir in dirs:
        for _, _, files in os.walk(os.path.join(root, dir)):
            for file in files:
                if file == 'editorial.md':
                    continue
                if not file.endswith('.md'):
                    continue
                with open(os.path.join(root, dir, file), 'r') as f:
                    contest_id = dir
                    if '-' in dir:
                        contest_id = dir.split('-')[0]
                        note = ' '.join(dir.split('-')[1:])
                        if note in ['skip', 'mathforces', 'no tutorial', 'april fools']:
                            continue
                    problem_id = file.split('.')[0]
                    if '-' in problem_id:
                        continue
                    print(contest_id, problem_id)
                    result = insert_db(contest_id, problem_id, f.read())
                    if result == 'success':
                        cnt.add((contest_id, problem_id))

for root, dirs, _ in os.walk('data/contests-v2'):
    for dir in dirs:
        for _, _, files in os.walk(os.path.join(root, dir)):
            for file in files:
                if file == 'editorial.md':
                    continue
                with open(os.path.join(root, dir, file), 'r') as f:
                    contest_id = dir
                    problem_id = file.split('.')[0]
                    print(contest_id, problem_id)
                    result = insert_db(contest_id, problem_id, f.read())
                    if result == 'success':
                        cnt.add((contest_id, problem_id))
                    else:
                        exit(0)

print(len(cnt))