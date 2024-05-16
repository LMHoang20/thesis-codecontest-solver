import helpers
import solver.train.prompts.debugger_public as public
import solver.train.prompts.debugger_private as private

from models import LLM
from logger import Logger

from entity.problem import Problem

class Debugger:
    def __init__(self, name: str, model: LLM, retry: int, logger: Logger = Logger()):
        self.name = name
        self.model = model
        self.retry = retry
        self.logger = logger

    def generate(self, problem: Problem, code: str, language: str, public: bool = False):
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
        prompt += public.task
        prompt += public.requirement
        prompt += public.answer_format
        prompt += public.format(problem.name, problem.tags, problem.rating, problem.description)
        prompt += public.format(problem.editorial)
        return helpers.remove_consecutive_line_breaks(prompt.strip())
    
    def validate_response_format(self, response):
        raise NotImplementedError