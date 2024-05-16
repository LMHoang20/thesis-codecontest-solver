task = """
# Task:
Given a problem statement and the editorial (an editorial is a solution written in natural language) for the problem, you have 2 tasks:
- ELABORATE: The solution contains a high level plan to solve the problem. You have to elaborate on the plan, and write a detailed step-by-step guide to implement the plan.
- CODE: Implement the plan in code. The code must be a full program that can be run without any extra code. 
"""

requirement = """
# What you MUST do:
- In the ELABORATE task:
    - You MUST write a detailed step-by-step guide to implement the plan.
    - You MUST write a 
    - The guide MUST be a bullet-point list of sentences.
    - The guide MUST be correct and complete.
- In the CODE task:
    - You MUST implement the plan in code.
    - The code MUST be a full program that can be run without any extra code.
    - The code MUST read from standard input and write to standard output.
    - The code MUST be in one of the following languages: C++, Python.
    - The code MUST follow the plan.
    - The code MUST be correct and pass all the test cases.
    - The code MUST be efficient and optimized.
    - The code MUST be easy to debug.
"""

answer_format = """
# Answer Format:
Your answer in each task MUST be a bullet-point list of sentences, each task MUST have a heading ELABORATE-TASK or CODING-TASK, and the tasks MUST be in the same order as mentioned in the problem statement.
Specifically, the format of the answer MUST be as follows:
// START OF FORMAT (MUST NOT contain this line)
ELABORATE-TASK:
- step 1: <high-level description of the action>
- step 2: <high-level description of the action>
    - step 2.1: <low-level description of the action>
    - step 2.2: <low-level description of the action>
- step 3: <high-level description of the action>
- ...
CODING-TASK:
Language: <language> (MUST be 'cpp' or 'python')
```<language> (MUST be the same as above)
<code>
```
// END OF FORMAT (MUST NOT contain this line)
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
// START OF EDITORIAL
{}
// END OF EDITORIAL
"""