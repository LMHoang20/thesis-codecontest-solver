import os
from inference import get_db_conn
from model import Gemini

def get_all_links():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	SELECT * FROM links
	''')
	rows = cursor.fetchall()
	cursor.close()
	
	return dict([
	(f'[{row[3]}]({row[0]})', (row[3], row[4], row[5])) for row in rows
	])

def replace_link_to_code(linkToCode, editorial):
	for link in linkToCode:
		if link in editorial:
			placeholder, code, language = linkToCode[link]
			editorial = editorial.replace(link, f"""
# TUTORIAL CODE XXX
```{language}
// Note: {placeholder}
{code}
```
""")
	return editorial


def get_all_problems_with_editorial(limit, offset):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute('''
	SELECT name, description, cf_contest_id, cf_index, cf_points, cf_rating, cf_tags, editorial FROM problems
	WHERE editorial != ''
	ORDER BY cf_contest_id, cf_index
	LIMIT %s OFFSET %s
	''', (limit, offset))
	rows = cursor.fetchall()
	cursor.close()
	return rows


def make_planning(model, name, description, rating, tags, editorial, code): 
	prompt = f"""
<TASK>
# Context:
You are a contestant in a programming contest. You are given a problem, its editorial, and a code solution.
Your task is to explain step by step the code in a way that another coder without the context can implement the same code.

# What to do:
- Focus on the logic and the flow of the program, in a DFS manner (if a function calls another function for the first time, explain the callee function before getting back to the caller function). Gloss over the details of the code.
- Make comment (if needed to be clarify) for a line by adding `#` at the end of the line. Not every line needs a comment.
- Simple loops, conditions, etc. should be explained in high level, in a single line. Simple concepts should also be condensed.
- If the code contains well known algorithms/data structures, only explain how to use them. If the code contains a modified version of a well known algorithm/data structure, note the modification.
- Treat a struct/class method call the same way as a function call.
- If a struct/class have special default values/constructors, the default values/constructors should be defined last, outside of the main function.
- If there is a function call in a condition, formula, another function call, etc. The function call should be extracted to a new line and the result should be stored in a variable.
- The code might contains multiple unused variables, functions, or even bugs, ignore them, and focus on the logic, loops, conditions, etc.
- Complicated math formulas, or any other complex logic should be copied as is.
- Output in the form of a customized, high level Python code written in DFS manner.

# For example:
Your answer should look something like this:
<ANSWER>
def main():
	n = int(input()) # an integer, 1 <= n <= 1e5
	a = list(map(int, input().split())) # a list of n integers, 1 <= a[i] <= 1e9
	segment_tree = SegmentTree(a) # a segment tree of a
	q = int(input()) # an integer, 1 <= q <= 1e5
	for i in range(q):
		k = int(input()) # an integer, 1 <= k <= 1e9
		l, r = 0, n
		ans = -1
		while l < r: # binary search
			mid = (l + r) // 2
			output_of_valid = valid(mid)
			def valid(mid):
				output_of_query = segment_tree.query(0, mid)
				def segment_tree.query(l, r):
					# well known segment tree query function
					# no need to explain
				return output_of_query >= k
			if output_of_valid:
				answer = mid
				r = mid - 1
			else:
				l = mid
		print(answer)

class SegmentTree:
	def __init__(self, a):
		self.tree = [0] * 4 * len(a)
		build(0, 0, len(a) - 1)
		def build(i, l, r):
			# well known segment tree build function
			# no need to explain
</ANSWER>

# Objective:
- The task is considered successful if the code can be re-implemented by another coder without the context.
</TASK>
<PROBLEM>
# Problem information:
- Name: {name}
- Rating: {rating}
- Tags: {tags}

# Problem description
{description}
</PROBLEM>
<EDITORIAL>
{editorial}
</EDITORIAL>
<CODE>
{code}
</CODE>
<ANSWER>
"""
	response = model.generate_content(prompt)
	assert len(response.candidates) == 1
	for candidate in response.candidates:
		print('------------------')
		assert len(candidate.content.parts) == 1
		print(candidate.content.parts[0].text)

cnt = 0
if __name__ == '__main__':
	offset = 0
	model = Gemini()
	linkToCode = get_all_links()
	while True:
		problems = get_all_problems_with_editorial(1, offset)
		if len(problems) == 0:
			break
		problem = problems[0]
		name, description, contest_id, problem_id, points, rating, tags, editorial = problem
		if contest_id == 1325 and problem_id == 'F':
			offset += 1
			continue
		editorial = editorial[editorial.find('\n') + 1:].strip()
		editorial = replace_link_to_code(linkToCode, editorial)
		sections = editorial.split('# TUTORIAL CODE XXX')
		if len(sections) > 1:
			cnt += 1
			# editorial = sections[0].strip()
			# for i in range(1, len(sections)):
				# code = sections[i].strip()
				# plan = make_planning(model, name, description, rating, tags, editorial, code)
		offset += 1
	print(cnt)
