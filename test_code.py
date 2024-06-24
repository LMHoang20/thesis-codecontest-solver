from database import get_db_conn
from repository import Problem
from sandbox import Judge
from helpers import get_session_id, parse_solution
from logger import get_logger

import random

def get_editorial():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, solutions
        FROM editorials_raw
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
def main():
    problem_repo = Problem(get_db_conn())
    editorials = get_editorial()
    session_id = get_session_id()
    logger  = get_logger(type='console')
    with open('code-passed.txt', 'r') as f:
        passed = f.readlines()
        passed = [x.strip() for x in passed]
    with open('code-failed.txt', 'r') as f:
        failed = f.readlines()
        failed = [x.strip() for x in failed if x not in passed]
    for name, solutions in editorials:
        if name in passed:
            continue
        assert type(solutions) == list and len(solutions) > 0
        solution = solutions[0]
        problem = problem_repo.get_problem(name)
        assert problem is not None
        judge = Judge('test-code', logger)
        tests = problem.get_tests()
        tests = random.choices(population=tests, k=10)
        code, language = parse_solution(solution)
        with open(f'tmp.{language}', 'w') as f:
            f.write(code)
        logger.info(f'testing {name}, tmp.{language}')
        result = judge.judge_tests(problem.name, code, language, tests)
        if result[0] != 'OK':
            logger.info(f'{name}, {result} failed')
            with open('code-failed.txt', 'a') as f:
                f.write(name)
                f.write('\n')
        else:
            with open('code-passed.txt', 'a') as f:
                f.write(name)
                f.write('\n')


if __name__ == '__main__':
    main()