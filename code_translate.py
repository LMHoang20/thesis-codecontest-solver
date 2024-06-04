import os

from sandbox import Judge
from database import get_db_conn
from models import get_llm_model
from logger import Logger

model = get_llm_model('gemini')
judge = Judge('translate', logger=Logger())

def translate_to_cpp(name, description, editorial, solution):
    # Prompt for translating the editorial to C++
    prompt_translation = f"Translate the following code to cpp, the result must be a full program that can be run without any extra code:\nProblem: {name}\nDescription: {description}\nEditorial: {editorial}\nSolution: {solution}"
    # Assuming the API call returns the translated text
    return model.generate(prompt_translation).strip()

def verify_cpp_translation(name, code, tests):
    if '```cpp' in code:
        code = code.split('```cpp')[1]
    if '```' in code:
        code = code.split('```')[0]
    return judge.judge_tests(name, code, 'cpp', tests)

def get_editorials():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT p.name, p.description, p.public_tests, p.private_tests, p.generated_tests, e.content, e.solutions FROM editorials e JOIN problems p ON e.name = p.name')
    return cur.fetchall()

def main():
    cnt = 0
    editorials = get_editorials()
    editorials = list(editorials)
    while len(editorials) > 0:
        name, description, public_tests, private_tests, generated_tests, content, solutions = editorials[0]
        editorials = editorials[1:]
        if not solutions:
            continue
        if os.path.exists(f'translated/{name}.cpp'):
            continue
        test_inputs = public_tests['input'] + private_tests['input'] + generated_tests['input']
        test_outputs = public_tests['output'] + private_tests['output'] + generated_tests['output']
        actual_tests = list(zip(test_inputs, test_outputs))
        solutions = [solution.strip() for solution in solutions]
        if any(solution.startswith('```cpp') or solution.startswith('```py') for solution in solutions):
            continue
        try:
            print(name)
            print(solutions[0])
            input()
            cnt += 1
            continue
            solution = solutions[0]
            code = translate_to_cpp(name, description, content, solution)
            print(code)
            result = verify_cpp_translation(name, code, actual_tests)
            if result[0] == 'OK':
                with open(f'translated/{name}.cpp', 'w') as f:
                    f.write(code)
            else:
                print(result[0])
                editorials.append((name, description, public_tests, private_tests, generated_tests, content, solutions))
            cnt += 1
        except Exception as e:
            print(e)
            editorials.append((name, description, public_tests, private_tests, generated_tests, content, solutions))
            continue
    print(cnt)
if __name__ == '__main__':
    main()