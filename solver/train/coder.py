import helpers

from models import LLM
from entity.problem import Problem
from logger import Logger

task = """
# Task:
Given a problem statement and the editorial (an editorial is a solution written in natural language) for the problem, you have 2 tasks:
- ELABORATE: The solution contains a high level plan to solve the problem. You have to elaborate on the plan, and write a detailed step-by-step guide to implement the plan.
- CODE: Implement the plan in code. The code must be a full program that can be run without any extra code. 
"""

requirement = """
# What you MUST do:
- In the EXTRACTION task:
    - Extract sentences from the problem statement that have one of the following properties:
        - the sentence contains input/output descriptions, or constraints (e.g. "1 ≤ N ≤ 10^5", "N is the length of the array", etc.)
        - the sentence describes a property of a unique entity in the problem (e.g "in one operation, Alice can increase the value of a number by 1", "the array is sorted in non-decreasing order", etc.)
        - the sentence contains information used by the editorial to solve the problem, also write what information is used, where it is used, and how it is used.
    - Ignore any irrelevant information (e.g. story telling sentences, context introduction, etc.)
- In the PLANNING task:
    - Write a plan for the implementation of the editorial. If the editorial contains multiple possible solutions/implementations, choose one (write out which solution you are choosing), and write a plan for that solution.
    - The plan should be a list of steps that you would take to implement the editorial.
    - Each step should be a high-level description of the actions you would take to implement the editorial.
    - The steps should be in the order that you would take them to implement the editorial.
    - Each step must be written in a way that is clear and easy to understand. So that the coder can easily understand the steps and implement the editorial.
- In the CODING task:
    - Write the code for the implementation based on the plan.
    - The code MUST be a full program that can be run without any extra code.
    - The code MUST be written in Python or C++.
"""

answer_format = """
# Answer Format:
Your answer in each task MUST be a bullet-point list of sentences, each task MUST have a heading EXTRACTION-TASK, PLANNING-TASK, CODING-TASK.
Specifically, the format of the answer MUST be as follows:
// START OF FORMAT
EXTRACTION-TASK:
- <sentence>. <why you extracted this sentence>
- <sentence>. <why you extracted this sentence>
- ...
PLANNING-TASK:
- <high-level description of the action>
- <high-level description of the action>
- ...
CODING-TASK:
```cpp or py
<code>
```
// END OF FORMAT
"""

problem_statement = """
# Problem Statement:
Name: {}
Tags: {}
Rating: {}
Description:
// START OF PROBLEM DESCRIPTION
{}
// END OF PROBLEM DESCRIPTION
"""

editorial = """
# Editorial:
{}
"""

accepted_languages = {
    'cpp': 
    [
        'cpp14', 'cpp17', 'cpp20', 'c++14', 'c++17', 'c++20', 'cpp', 'c++', 'c',
    ], 
    'python': 
    [
        'python3', 'python2', 'python', 'py3', 'py2', 'py',
    ]
}

class Coder:
    def __init__(self, model: LLM, retry: int, logger: Logger):
        self.model = model
        self.retry = retry
        self.logger = logger
    def generate(self, problem: Problem) -> str:
        assert type(problem.editorial) == str and problem.editorial != None and problem.editorial != ""
        retry = 0
        prompt = self.make_prompt(problem)
        self.logger.info("[Coder] Generating code for problem:", problem.name)
        while retry < self.retry:
            try:
                response = self.model.generate_content(prompt)
                self.logger.info("[Coder] Response:", response)
                if not self.validate_response_format(response):
                    raise Exception("invalid response format")
                return self.parse(response)
            except Exception as e:
                self.logger.error("[Coder] Error:", e)
                retry += 1
    def make_prompt(self, problem: Problem) -> str:
        prompt = ""
        prompt += task
        prompt += requirement
        prompt += answer_format
        prompt += problem_statement.format(problem.name, problem.tags, problem.rating, problem.description)
        prompt += editorial.format(problem.editorial)
        return helpers.remove_consecutive_line_breaks(prompt)
    def validate_response_format(self, response: str) -> bool:
        if 'EXTRACTION-TASK:' not in response:
            return False
        if 'PLANNING-TASK:' not in response:
            return False
        if 'CODING-TASK:' not in response:
            return False
        code_task = response.split('CODING-TASK:')[1].strip()
        if '```' not in code_task:
            return False
        cnt = 0
        for lang in accepted_languages:
            if any(f'```{lang}' in code_task for lang in lang):
                cnt += 1
        return cnt == 1
    def parse(self, response: str) -> str:
        response = response.strip()
        for language, variants in accepted_languages.items():
            for variant in variants:
                if f'```{variant}' in response:
                    code = response.split(f'```{variant}')[1].strip()
                    if '```' in code:
                        code = code.split('```')[0].strip()
                    return code, language