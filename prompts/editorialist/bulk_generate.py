from entity.problem import Problem

task = """# Task:
Given a competitive programming problem statement, help me brainstorm exactly {} editorials for the problem.
Each editorial must be unique, different from the others.
Each editorial must be writen as if it is unaware of the other editorials.
"""

output_format = """# Format:
Your output MUST be in the yaml format:
The root is a dictionary with one key: editorials.
The value of editorials is a list of dictionaries.
Each dictionary represents an editorial.
Each editorial has 3 keys: index, analyze, and planning.
The value of index is a number.
The value of analyze is a multiline string that contains the mathematical reasoning, observation, fact, etc.
The value of planning is a multiline string that contains the plan of implementation and the complexity of the solution.
```yaml
---
editorials:
	- index: <index>
	  analyze: |
		<your analysis>
	  planning: |
		<your plan>
	- index: <index>
	  analyze: |
		<your analysis>
	  planning: |
		<your plan>
```
"""

input_statement = """```yaml
---
name: {}
tags: {}
description: |
{}
```
"""

def get_prompt(number_of_editorials: int, problem: Problem):
    if type(problem.tags) == str:
        tags = problem.tags
    elif type(problem.tags) == list:
        tags = ', '.join(problem.tags)
    else:
        print('Invalid tags type')
        tags = ''
    return [
        task.format(number_of_editorials) + output_format,
        input_statement.format(problem.name, tags, problem.description),
        '```yaml\n---\neditorials:\n'
    ]