from models import LLM
from entity import Problem

prompt_template = """# Task:
Given a problem statement, write the editorial for the problem.
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
    def __init__(self, model: LLM, retry: int = 3):
        self.model = model
        self.retry = retry
    def generate(self, problem: Problem) -> str:
        retry = 0
        while retry < self.retry:
            try:
                prompt = self.make_prompt(problem)
                response = self.model.generate_content(prompt)
                if not self.validate_idea_format(response):
                    raise Exception("invalid response format")
                return self.parse_idea(response)
            except Exception as e:
                retry += 1
    def make_prompt(self, problem: Problem) -> str:
        pass
    def validate_idea_format(self, idea: str) -> bool:
        pass
    def parse_idea(self, response: str) -> str:
        pass

class GroundTruth(Editorialist):
    def generate(self, problem: Problem) -> str:
        return problem.editorial
    def make_prompt(self, problem: Problem) -> str:
        raise NotImplementedError
    def validate_idea_format(self, idea: str) -> bool:
        return True
    def parse_idea(self, response: str) -> str:
        raise NotImplementedError
