import models
import repository

from psycopg2.extras import Json
from entity.problem import Problem
from database import get_db_conn
from helpers import get_session_id
from coder import Coder
from editorialist import Editorialist, GroundTruth, OneShot
from sandbox import Judge, Checker
from models import LLM
from logger import Logger, get_logger
from debugger import Debugger

class BetaCode:
    def __init__(self, name: str, editorialist: Editorialist, coder: Coder, judge: Judge, debugger: Debugger, logger: Logger = Logger()):
        self.name = name
        self.editorialist = editorialist
        self.coder = coder
        self.judge = judge
        self.debugger = debugger
        self.logger = logger
        self.total_llm_calls = 0
        self.max_total_llm_calls = 20
    def call_llm(self, llm: LLM, *args, **kwargs):
        if self.total_llm_calls >= self.max_total_llm_calls:
            raise Exception("maximum total llm calls reached")
        self.total_llm_calls += 1
        return llm.generate(*args, **kwargs)

    def solve(self, problem: Problem):
        try:
            self.logger.info("generating editorial for problem:", problem.name)
            problem.editorial = self.call_llm(self.editorialist, problem=problem)
            self.logger.info("generating code for problem:", problem.name)
            result = self.call_llm(self.coder, problem=problem)
            code, language = result
            tests = problem.get_tests(public=True, private=False, generated=False)
            self.logger.info("public judge code for problem:", problem.name)
            judge_result = self.judge.judge_tests(problem.name, code, language, tests)
            while judge_result[0] != 'OK':
                code = self.debugger.generate(code, language, public=True)
                judge_result = self.judge.judge_tests(tests)
            tests = problem.get_tests(public=True, private=True, generated=True)
            while judge_result[0] != 'OK':
                code = self.debugger.generate(code, language, public=False)
                judge_result = self.judge.judge_tests(tests)
            return code, language
        except Exception as e:
            return "", "", ("ERROR", str(e))

def main():
    model = models.get_llm_model('gemini')
    # problem = get_problem(name)
    problem_repo = repository.Problem(get_db_conn())
    problems = problem_repo.get_test_problems(split='test')
    for problem in problems:
        session_id = get_session_id()
        
        # logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/beta-code.log', 'threadsafe': False})
        editorialist_logger = get_logger(type='console', config={'name': session_id + '-editorialist', 'threadsafe': False})
        coder_logger = get_logger(type='console', config={'name': session_id + '-coder', 'threadsafe': False})
        judge_logger = get_logger(type='console', config={'name': session_id + '-judge', 'threadsafe': False})
        debugger_logger = get_logger(type='console', config={'name': session_id + '-debugger', 'threadsafe': False})
        system_logger = get_logger(type='console', config={'name': session_id + '-system', 'threadsafe': False})
        
        # editorialist = GroundTruth(session_id, model, RETRY_EDITORIAL, editorialist_logger)
        editorialist = OneShot(session_id, model, editorialist_logger)
        coder = Coder(session_id, model, coder_logger)
        judge = Judge(session_id, judge_logger)
        debugger = Debugger(session_id, model, debugger_logger)
        betaCode = BetaCode(session_id, editorialist, coder, judge, debugger, system_logger)
        
        code, language, result = betaCode.solve(problem)
        if result[0] == 'OK':
            with open(f'solutions/{problem.contest_id}_{problem.problem_id}.{language}', 'w') as f:
                f.write(code)
            with open(f'solutions/{problem.contest_id}_{problem.problem_id}.txt', 'w') as f:
                f.write(problem.editorial)

if __name__ == '__main__':
    main()

# 1743