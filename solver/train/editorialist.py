from models import LLM, LLMHandler, get_llm_model
from entity.problem import Problem
from logger import Logger, ConsoleLogger
from database import get_db_conn
from prompts.iterative_editorialist import iterative_generator_template, iterative_verifier_template

prompt_template = """# Task:
Given a problem statement, write the editorial in natural language without coding for the problem.
The editorial MUST be a line-by-line 
{}
"""

statement_template = """## Name:
{}
## Tags:
{}
## Description:
{}
"""

class Editorialist:
    def generate(self, problem: Problem) -> str:
        raise NotImplementedError

class OneShot(Editorialist):
    def __init__(self, name: str, model: LLM, retry: int, logger: Logger):
        self.name = name
        self.model = model
        self.retry = retry
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        prompt = self.make_prompt(problem)
        response = self.model.generate(prompt)
        if not self.validate_idea_format(response):
            raise Exception("invalid response format")
        return self.parse_idea(response)
    def make_prompt(self, problem: Problem) -> str:
        return prompt_template.format(statement_template.format(problem.name, ', '.join(problem.tags), problem.description))
    def validate_idea_format(self, idea: str) -> bool:
        return True
    def parse_idea(self, response: str) -> str:
        return response

class GroundTruth(Editorialist):
    def __init__(self, name: str, logger: Logger):
        self.name = name
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        assert type(problem.editorial) == str and problem.editorial != None and problem.editorial != ""
        return problem.editorial

class FetchGenerated(Editorialist):
    def __init__(self, name: str, logger: Logger):
        self.name = name
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        assert type(problem.name) == str and len(problem.name) > 0
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT generated
            FROM generated_editorials
            WHERE name = %s
        """, (problem.name,))
        editorial = cursor.fetchone()
        assert editorial != None
        editorial = editorial[0]
        assert type(editorial) == str and editorial != None and editorial != ""
        cursor.close()
        return editorial
    
class Iterative(Editorialist):
    def __init__(self, name: str, model: LLM, retry: int, logger: Logger):
        self.name = name
        self.generator = LLMHandler(model, iterative_generator_template())
        self.verifier = LLMHandler(model, iterative_verifier_template())
        self.retry = retry
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        retry = 0
        while retry < self.retry:
            try:
                prompt = self.generator.make_prompt(problem.name, ', '.join(problem.tags), problem.description)
                print(prompt)
                response = self.generator.generate(prompt)
                return response
            except Exception as e:
                self.logger.error(self.name, e)
                retry += 1
        return None

def get_test_problems():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
        FROM testing_problems
        ORDER BY cf_rating, name
    """)
    problems = cursor.fetchall()
    cursor.close()
    conn.close()
    print("total problems:", len(problems))
    for problem in problems:
        yield Problem(name=problem[0], description=problem[1], rating=problem[2], tags=problem[3], source='codeforces', public_tests=problem[4], private_tests=problem[5], generated_tests=problem[6], contest_id=problem[7], problem_id=problem[8])


if __name__ == "__main__":
    model = get_llm_model('gemini')
    editorial = Iterative("iterative", model, 3, ConsoleLogger())
    problems = get_test_problems()
    for problem in problems:
        print(editorial.generate(problem))