from models import LLM
from entity.problem import Problem
from logger import Logger

class Editorialist:
    def generate(self, problem: Problem) -> str:
        raise NotImplementedError

class BulkGenerator(Editorialist):
    def __init__(self, name: str, model: LLM, logger: Logger):
        self.name = name
        self.model = model
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