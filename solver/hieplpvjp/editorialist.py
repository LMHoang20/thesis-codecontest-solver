import repository
import yaml

from typing import List
from models import LLM, get_llm_model
from entity.problem import Problem
from logger import Logger
from database import get_db_conn
from prompts.editorialist import bulk_generate

class Editorialist(LLM):
    def generate(self, problem: Problem) -> str:
        raise NotImplementedError

class BulkGenerator(Editorialist):
    def __init__(self, name: str, model: LLM, logger: Logger = Logger()):
        self.name = name
        self.model = model
        self.logger = logger
    def generate(self, problem: Problem) -> List[str]:
        prompt = self.make_prompt(problem)
        print('\n'.join(prompt))
        response = self.model.generate(prompt)
        response = prompt[-1] + response
        print(response)
        self.logger.info(f"generated response for problem: {problem.name}")
        return self.parse_idea(response)
    def make_prompt(self, problem: Problem) -> str:
        return bulk_generate.get_prompt(5, problem)
    def parse_idea(self, response: str) -> str:
        if response.startswith("```yaml"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        editorials = yaml.safe_load(response)
        return editorials
    
if __name__ == "__main__":
    problem_repo = repository.Problem(get_db_conn())
    problem = problem_repo.get_problem('1559_A. Mocha and Math')
    model = get_llm_model('gemini')
    editorialist = BulkGenerator("bulk-generator", model)
    editorials = editorialist.generate(problem)
    for i, editorial in enumerate(editorials['editorials']):
        print('Editorial', i+1)
        print('analyze:', editorial['analyze'])
        print('planning:', editorial['planning'])
        print('---------------------')
