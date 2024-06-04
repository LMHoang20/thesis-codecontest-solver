import os 
import re
import subprocess

def get_tag(content, tag):
    start_tag = f'<{tag}-START>'
    end_tag = f'<{tag}-END>'
    start = content.find(start_tag)
    end = content.find(end_tag)
    if start == -1 or end == -1:
        return None
    return content[start + len(start_tag):end].strip()

def main():
    contest_ids = []

    with open('review-1.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            contest_id, status = line.split(': ')
            if status.strip() == 'ok':
                contest_ids.append(contest_id)

    for contest_id in contest_ids:
        print(f'Processing {contest_id}...')
        with open(f'data/prompts/{contest_id}/editorial.md', 'r') as f:
            required = f.read()
            required = get_tag(required, 'REQUIRED')
            print(f'Required:\n{required}')
        with open(f'data/contests-v2/{contest_id}/editorial.md', 'r') as f:
            editorial = f.read()
            with open(f'tmp_editorial.md', 'w') as f:
                f.write(editorial)
        with open(f'data/prompts/{contest_id}/editorial-generated.md', 'r') as f:
            data = f.read()
        with open(f'tmp_data.md', 'w') as f:
            f.write(data)
        answers = get_tag(data, 'ANSWER')
        if answers == None:
            answers = data
        print(f'Answers:\n{answers}')
        with open(f'tmp_answers.md', 'w') as f:
            f.write(answers)
        answers = answers.split('\n')
        for i in range(len(answers)):
            problem_start = editorial.find(answers[i])
            problem_end = len(editorial)
            if i < len(answers) - 1:
                problem_end = editorial.find(answers[i + 1])
            problem = editorial[problem_start:problem_end].strip()
            while '\n\n\n' in problem:
                problem = problem.replace('\n\n\n', '\n\n')
            with open(f'tmp_answer.md', 'w') as f:
                f.write(problem)
            while True:
                command = input().strip()
                if command == 'exit':
                    exit(0)
                elif command == 'skip':
                    print('Skipping...')
                    break
                elif command.startswith('save'):
                    with open(f'tmp_answer.md', 'r') as f:
                        problem = f.read()
                    name = command.split()[1]
                    with open(f'data/contests-v2/{contest_id}/{name}.md', 'w') as f:
                        f.write(problem)
                    print(f'Wrote to {name}.md')
                    break
                elif command.startswith('process'):
                    if 'no-formula' not in command:
                        os.system(f'python process_latex.py tmp_answer.md')
                    else:
                        os.system(f'python process_latex_no_formula.py tmp_answer.md')
                else:
                    print('Invalid command')

if __name__ == '__main__':
    main()