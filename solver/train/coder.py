import helpers
import prompts.coder as coder_prompts

from typing import Tuple
from models import LLM
from entity.problem import Problem
from logger import Logger

class Coder:
    def __init__(self, name: str, model: LLM, retry: int, logger: Logger = Logger()):
        self.name = name
        self.model = model
        self.retry = retry
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        assert type(problem.editorial) == str and problem.editorial != None and problem.editorial != ""
        retry = 0
        prompt = self.make_prompt(problem)
        self.logger.info("prompt:", prompt)
        self.logger.info("generating code for problem:", problem.name)
        while retry < self.retry:
            try:
                response = self.model.generate(prompt)
                self.logger.info("response:", response)
                result, error = self.validate_response_format(response)
                if not result:
                    raise Exception("invalid response format" + error)
                return self.parse(response)
            except Exception as e:
                self.logger.error(self.name, e)
                retry += 1
        return None
    def make_prompt(self, problem: Problem) -> str:
        prompt = ""
        prompt += coder_prompts.task
        prompt += coder_prompts.requirement
        prompt += coder_prompts.answer_format
        prompt += coder_prompts.problem_statement.format(problem.name, problem.tags, problem.rating, problem.description)
        prompt += coder_prompts.editorial.format(problem.editorial)
        return helpers.remove_consecutive_line_breaks(prompt.strip())
    def validate_response_format(self, response: str) -> bool:
        response = response.replace('// START OF FORMAT (MUST NOT contain this line)', '')
        response = response.replace('// END OF FORMAT (MUST NOT contain this line)', '')
        response = response.strip()
        if 'ELABORATE-TASK:' not in response:
            return False, 'ELABORATE-TASK not found'
        if 'CODING-TASK:' not in response:
            return False, 'CODING-TASK not found'
        code_task = response.split('CODING-TASK:')[1].strip()
        if not code_task.startswith('Language:'):
            return False, 'language not found'
        language = code_task.split('\n')[0].split(':')[1].strip()
        if language not in ['cpp', 'python']:
            return False, 'invalid language'
        code = code_task.split('\n', 1)[1].strip()
        if not code.startswith('```'):
            return False, 'code start not found'
        # if not code.endswith('```'):
            # return False, 'code end not found'
        if not code.startswith(f'```{language}\n'):
            return False, 'invalid code language'
        return True, ''
    def parse(self, response: str) -> Tuple[str, str]:
        response = response.replace('// START OF FORMAT (MUST NOT contain this line)', '')
        response = response.replace('// END OF FORMAT (MUST NOT contain this line)', '')
        response = response.strip()
        code_task = response.split('CODING-TASK:')[1].strip()
        language = code_task.split('\n')[0].split(':')[1].strip()
        code = code_task.split('\n', 1)[1].strip()
        code = code.split(f'```{language}')[1]
        code = code.split('```')[0]
        code = code.strip()
        return code, language
        

