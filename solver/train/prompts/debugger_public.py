common_mistakes = [
    "- Floor and ceil division: The code is not handling the division correctly.",
    "- Number overflow: The code is not handling the large numbers correctly.",
    "- Off by one error: The code is not handling the edge cases correctly."
]

task = """
# Task:
Given a problem statement, the solution reasoning, the flawed code, and the failed test cases, you have 3 tasks:
- IDENTIFY: Identify the mistakes in the flawed solution, both in the reasoning and the code.
- PLANNING: Re-write a detailed step-by-step guide to implement the correct solution.
- CODING: Implement the corrected solution in code.
"""

requirement = """
- In the IDENTIFY task:
    - Identify whether the mistakes is in the code or the reasoning.
        - If the code is not implemented correctly, then the mistake is in the code.
            - You MUST go through all of these common mistakes and identify the one that is present in the code.
{}
        - If the code correctly implements the step-by-step guide in the reasoning, and still get the wrong answer, then the mistake is in the reasoning.
            - You MUST identify the step in the reasoning that is incorrect.
    - You MUST write a detailed explanation of the mistake.
- In the PLANNING task:
"""

answer_format = """
# Answer Format:
Your answer in each task MUST be a bullet-point list of sentences, each task MUST have a heading EXTRACTION-TASK, PLANNING-TASK, CODING-TASK.
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