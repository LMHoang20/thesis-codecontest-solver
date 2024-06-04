import os

for _, dirs, _ in os.walk('data/contests'):
    examines = []
    for dir in dirs:
        if '-' in dir:
            contest_id = dir[:dir.find('-')]
            note = dir[dir.find('-')+1:]
        else:
            contest_id = dir
            note = ''
        if (int(contest_id) >= 1338 or note == 'yes-code') and int(contest_id) >= 1342:
            examines.append((contest_id, note))
    examines = sorted(examines, key=lambda x: int(x[0]))
    print(len(examines))    
    for contest_id, note in examines:
        dir = contest_id
        if note != '':
            dir += f'-{note}'
        print(dir)
        for _, _, files in os.walk(f'data/contests/{dir}'):
            for file in files:
                if file == 'editorial.md':
                    continue
                if '-' in file:
                    problem_index = file[:file.find('-')]
                    problem_note = file[file.find('-')+1:-3]
                else:
                    problem_index = file[:-3]
                    problem_note = ''
                print(problem_index, problem_note)
                with open(f'data/contests/{dir}/{file}', 'r') as f:
                    problem = f.read()
                with open('tmp_answer.md', 'w') as f:
                    f.write(problem)
                with open(f'data/contests/{dir}/editorial.md', 'r') as f:
                    editorial = f.read()
                problem = problem[problem.find('\n'):].strip()
                sus = ''
                last_found = -1
                for c in problem:
                    sus += c
                    if editorial.find(sus) == -1:
                        break
                    else:
                        last_found = editorial.find(sus)
                if last_found == -1:
                    with open('tmp_editorial.md', 'w') as f:
                        f.write(editorial)
                else:
                    with open('tmp_editorial.md', 'w') as f:
                        f.write(editorial[last_found:last_found+1000])
                cnt = 2000
                while True:
                    command = input().strip()
                    if command == 'save':
                        with open('tmp_answer.md', 'r') as f:
                            problem = f.read()
                        with open(f'data/contests-v2/{contest_id}/{file}', 'w') as f:
                            f.write(problem)
                        break
                    elif command == 'm':
                        with open('tmp_editorial.md', 'w') as f:
                            f.write(editorial[last_found:last_found+cnt])
                        cnt += 1000
                    elif command == 'all':
                        with open('tmp_editorial.md', 'w') as f:
                            f.write(editorial)
                    elif command == 'skip':
                        break
                    elif command == 'p':
                        os.system('python process_latex.py tmp_answer.md')
                    else:
                        print('Invalid command')
            