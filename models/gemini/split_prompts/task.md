<TASK>
Context:
You are given an editorial for a code contest. The editorial might contains multiple solutions to the problems in the contest. Solution are usually separated by their names/titles, the next solution starts when the previous solution ends. Each solution in the editorial might contains the title, a natural language tutorial and maybe some snippets of code. 

Task:
- Your task is to find from the editorial the solution for a specific problem, specified in between the <TARGET> and </TARGET> tag. The name of the problem is IMPORTANT. 
- If the problem name is not found in the editorial, or if there are no solution for the problem, answer with "NO SOLUTION". 
- If the solution exists, extract the entire tutorial (including the snippets of code if exists) for the problem and provide it as the answer.

Structure:
- Your entire answer should be wrapped in the <ANSWER> and </ANSWER> tags.
- Start the answer with the name of the problem, wrapped in the <NAME> and </NAME> tags.
- Followed by the tutorial for the problem, wrapped in the <TUTORIAL> and </TUTORIAL> tags.

Note:
- COPY FULLY AND EXACTLY THE CONTENT OF THE SOLUTION IN THE EDITORIAL. DO NOT MODIFY THE CONTENT.
</TASK>