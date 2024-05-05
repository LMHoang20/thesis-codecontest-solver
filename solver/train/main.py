import models

from entity.problem import Problem
from database import get_db_conn
from helpers import get_session_id
from coder import Coder
from editorialist import Editorialist
from sandbox import Judge, Checker
from models import LLM
from logger import Logger, get_logger
from debugger import Debugger


RETRY_EDITORIAL = 3
RETRY_CODER = 3
RETRY_DEBUGGER = 3

class BetaCode:
    def __init__(self, editorialist: Editorialist, coder: Coder, judge: Judge, debugger: Debugger):
        self.editorialist = editorialist
        self.coder = coder
        self.judge = judge
        self.debugger = debugger
    def solve(self, model: LLM, problem: Problem, logger: Logger = None):
        try:
            problem.editorial = self.editorialist.generate(problem)
            code, language = self.coder.generate(problem)
            tests = problem.get_tests()
            judge_result = self.judge.judge_tests(tests)
            while judge_result[0] != 'OK':
                debugger = Debugger(model, RETRY_DEBUGGER)
                code = debugger.debug(code, language)
            return code, language
        except Exception as e:
            return str(e)

def get_random_problem():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, description, cf_rating, cf_tags, source, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
        FROM problems
        WHERE editorial != ''
        AND description NOT LIKE '%print any%'
        AND description NOT LIKE '%<image>%'
        AND NOT '*special' = ANY(cf_tags)
        AND NOT 'interactive' = ANY(cf_tags)
        AND cf_rating = 800
        ORDER BY RANDOM() LIMIT 1
    """)
    problem = cursor.fetchone()
    cursor.close()
    conn.close()
    return Problem(name=problem[0], description=problem[1], rating=problem[2], tags=problem[3], source=problem[4], public_tests=problem[5], private_tests=problem[6], generated_tests=problem[7], contest_id=problem[8], problem_id=problem[9])
    

def main():
    session_id = get_session_id()
    model = models.get_llm_model('gemini')
    problem = get_random_problem()
    logger = get_logger(type='file', config={'name': session_id, 'path': 'logs/beta-code.log', 'threadsafe': False})
    betaCode = BetaCode()
    betaCode.solve(model, problem, logger)

if __name__ == '__main__':
    main()