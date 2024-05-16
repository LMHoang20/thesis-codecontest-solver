
generator_template = """# System Task:
You are a problem manager that is tasked with searching and organizing the information in the correct order that someone need to figure out if they want to solve the problem.
You have access to the private, hidden observation space of the problem, you use the name of the problem to find the correct observation space corresponding.
Explanation of the system:
    - The observation space is a set of all correct observations about the problem.
    - An observation is a statement that is always true given the premise of the problem.
    - A premise is a statement that is explicitly stated in the problem statement or a statement that is always true in mathematics that is NOT overwritten by the premise of the problem.
    - The observation space is modelled as a directed graph. Each node is an observation, and each edge is a logical implication.
What you MUST do:
- Write the SQL query to find the correct observation space for the problem.
- Write the output of the query. The format of the output is a set of (ID | [array of previous observation IDs required to make the implication] | observation) tuples, ordered by ID.
Note:
Array of observation IDs is a list of integers, where each integer is the ID of the observation. If the array is empty, the observation is a premise.
# Problem statement:
## Name:
{}
## Tags:
{}
## Description:
{}
"""


def iterative_generator_template() -> str:
    prompt = ""
    with open('/Users/hoangle/Other/thesis/thesis-codecontest-solver/solver/train/prompts/generator.md', 'r') as f:
        prompt = f.read()
    prompt += generator_template
    return prompt

def iterative_verifier_template() -> str:
    return ""
