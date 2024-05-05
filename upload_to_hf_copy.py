import helpers
import datasets

from huggingface_hub import login
from database import get_db_conn
from entity.problem import Problem
from constants import *

unicode_replace = {
	'\u2009': ' ',
	'\u200b': '',
	'\u2002': ' ',
	'’': "'",
	'\xa0': ' ',
	'\u2061': '',
	'А': 'A',
	'“': '"',
	'р': 'p',
	'’': "'",  
	'і': 'i',
	'с': 'c',
	'х': 'x',
	'у': 'y',
	'м': 'm',
	'а': 'a',
	'С': 'C',
	'”': '"',
	'‘': "'",
	'…': '...',
	'е': 'e',
	'о': 'o',
	'—': '-',
	'–': '-',
	'−': '-',
	'и': ' and ',
	'′': "'",
	'，': ',',
	'⋅': '·',
	'-  >': '\\to',
	'{i * }': '{i*}',
}
latex_replace = {
	'\\le': '≤',
	'\\ge': '≥',
	'\\cdots': '...',
	'\\ldots': '...',
	'\\dots': '...',
	'\\cdot': '·',
	'\\times': '×',
	'\\div': '÷',
	'\\leq': '≤',
	'\\geq': '≥',
	'\\neq': '≠',
	'\\infty': '∞',
	'\\notin': '∉',
	'\\subset': '⊂',
	'\\in': '∈',
	'\\forall': '∀',
	'\\exists': '∃',
	'\\nexists': '∄',
	'\\emptyset': '∅',
	'\\varnothing': '∅',
	'\\cup': '∪',
	'\\cap': '∩',
	'\\supset': '⊃',
	'\\subseteq': '⊆',
	'\\supseteq': '⊇',
	'\\subsetneq': '⊊',
	'\\supsetneq': '⊋',
	'\\setminus': '∖',
	'\\backslash': '∖',
	'\\triangle': '△',
	'\\nabla': '∇',
	'\\partial': '∂',
	'\\angle': '∠',
	'\\parallel': '∥',
	'\\perp': '⊥',
	'\\cong': '≅',
	'\\equiv': '≡',
	'\\approx': '≈',
	'\\simeq': '≃',
	'\\sim': '∼',
	'\\propto': '∝',
	'\\varepsilon': 'ε',
	'\\epsilon': 'ε',
	'\\bigcup': '⋃',
	'\\lfloor': '⌊',
	'\\rfloor': '⌋',
	'\\langle': '⟨',
	'\\rangle': '⟩',
	'\\sigma': 'σ',
	'\\lvert': '|',
	'\\rvert': '|',
	'\\Sigma': 'Σ',
	'\\cfrac': '\\frac',
	'\\delta': 'δ',
	'\\oplus': '⊕',
	'\\Omega': 'Ω',
	'\\wedge': '∧',
	'\\rceil': '⌉',
	'\\lceil': '⌈',
	'\\colon': ':',
	'\\omega': 'ω',
	'\\prime': "'",
	'\\dfrac': '\\frac',
	'\\gamma': 'γ',
	'\\vdots': '⋮',
	'\\Phi': 'Φ',
	'\\gt': '>',
	'\\lt': '<',
	'\\pi': 'π',
	'\\pm': '±',
	'\\to': '→',
	'\\ll': '≪',
	'\\mu': 'μ',
	'\\ln': 'log',
	'\\ne': '≠',
	'\\nmid': '∤',
	'\\eta': 'η',
	'\\tau': 'τ',
	'\\rho': 'ρ',
	'\\ell': 'l',
	'\\phi': 'φ',
	'\\neg': '¬',
	'\\deg': '°',
	'\\circ': '°',
	'\\vert': '|',
	'\\tilde': '~',
	'\\alpha': 'α',
	'\\beta': 'β',
	'\\Bigr': '',
	'\\land': '∧',
	'\\bigcap': '⋂',
	'\\lambda': 'λ',
	'\\limits': '',
	'\\mapsto': '↦',
	'\\varphi': 'φ',
	'\\geqslant': '≥',
	'\\leftarrow': '←',
	'\\Theta': 'Θ',
	'\\Delta': 'Δ',
	'\\tfrac': '\\frac',
	'\\Bigl': '',
	'\\vee': '∨',
	'\\not': '¬',
	'\\Z': 'ℤ',
	'\\Big': '',
	'\\big': '',
	'\\bigg': '',
	'\\biggl': '',
	'\\Biggr': '',
	'\\Bigl': '',
	'\\Bigg': '',
	'\\mid': '|',
	'\\iff': '⇔',
	'\\implies': '⇒',
	'\\p': 'p',
	'\\quad': ' ',
	'\\space': ' ',
	'\\textrm': '\\text',
	'\\textbf': '\\text',
	'\\textit': '\\text',
	'\\texttt': '\\text',
	'\\mathsf': '\\mathsf',
	'\\,': ' ',
	'\\;': ' ',
	'\\:': ' ',
	'\\!': ' ',
}

def remove_unescaped_dollars(editorial: str) -> str:
	new_editorial = ''
	offset = 0
	dollars = [-1]
	while '$' in editorial[offset:]:
		index = editorial.index('$', offset)
		if not escaped(editorial, index):
			dollars.append(index)
		offset = index + 1
	dollars.append(len(editorial))
	for i, j in zip(dollars, dollars[1:]):
		new_editorial += editorial[i + 1: j]
	return new_editorial

def get_match_code(name):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT code, language
	FROM matches
	WHERE name = %s
	ORDER BY score DESC, session_id DESC
	LIMIT 1
	""", (name,))
	match = cursor.fetchone()
	cursor.close()
	return match

def get_problem(name):
	print(name)
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name, p.description, p.cf_tags, p.cf_rating, s.problem_understanding, s.solution_reasoning, s.implementation_planning
	FROM problems p
	JOIN summaries_v3 s ON p.name = s.name
	WHERE p.name = %s
	""", (name,))
	problem = cursor.fetchone()
	cursor.close()
	problem_understanding = problem[4]
	solution_reasoning = problem[5]
	implementation_planning = problem[6]
	problem_understanding_text = ""
	for line in problem_understanding.split('\n'):
		if 'REASON:' in line:
			line = line.split('REASON:')[0].rstrip()
		if len(line.strip()) < 2:
			continue
		if line.lstrip().startswith('- '):
			if line.startswith('- '):
				line = line[2:]
				problem_understanding_text += ' ' + line.strip('*').strip('"')
			else:
				problem_understanding_text += '\n' + line[:line.index('-')] + line[line.index('-') + 2:].strip('*').strip('"')
			if problem_understanding_text[-1] != '.':
				problem_understanding_text += '.'
		else:
			raise Exception(f"Unexpected line: {line}")
	solution_reasoning_text = ""
	for line in solution_reasoning.split('\n'):
		if 'REASON:' in line:
			line = line.split('REASON:')[0].rstrip()
		if len(line.strip()) < 2:
			continue
		if line.lstrip().startswith('- '):
			if line.startswith('- '):
				line = line[2:]
				solution_reasoning_text += ' ' + line.strip('*').strip('"')
			else:
				solution_reasoning_text += '\n' + line[:line.index('-')] + line[line.index('-') + 2:].strip('*').strip('"')
			if solution_reasoning_text[-1] != '.':
				solution_reasoning_text += '.'
		else:
			raise Exception(f"Unexpected line: {line}")
	implementation_planning_text = ""
	for line in implementation_planning.split('\n'):
		if 'REASON:' in line:
			line = line.split('REASON:')[0].rstrip()
		if len(line.strip()) < 2:
			continue
		if line.lstrip().startswith('- '):
			if line.startswith('- '):
				line = line[2:].strip('*').strip('"')
				implementation_planning_text += '\n' + line
			else:
				line = line[:line.index('-')] + line[line.index('-') + 2:].strip('*').strip('"')
				implementation_planning_text += '\n' + line
			if implementation_planning_text[-1] != '.':
				implementation_planning_text += '.'
		else:
			if line == '// END OF ANSWER':
				continue
			if line == '// END OF SOLUTION':
				continue
			raise Exception(f"Unexpected line: {line}")
	editorial = f"Let's summarize the problem.{problem_understanding_text}\nLet's make some observation.{solution_reasoning_text}\nSo the plan is:\n{implementation_planning_text}"
	editorial = helpers.remove_consecutive_line_breaks(editorial)
	editorial = remove_unescaped_dollars(editorial)
	return Problem(name=problem[0], description=problem[1], editorial=editorial, code='', tags=problem[2], rating=problem[3], source='codeforces')
	

def get_problem_names():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name
	FROM problems p
	JOIN summaries_v3 s ON p.name = s.name
	ORDER BY p.cf_rating ASC
	""")
	problems = cursor.fetchall()
	conn.close()
	return problems

def escaped(editorial: str, index: int) -> bool:
	for i in range(index - 1, -1, -1):
		if editorial[i] != '\\':
			return (index - i) % 2 == 0
	return False

def replace_one(editorial: str, control_sequence: str, symbol: str) -> str:
	new_editorial = ''
	offset = 0
	while control_sequence in editorial[offset:]:
		index = editorial.index(control_sequence, offset)
		if escaped(editorial, index):
			new_editorial += editorial[offset: index + len(control_sequence)]
			offset = index + len(control_sequence)
			continue
		if editorial[index + len(control_sequence)].isalpha():
			new_editorial += editorial[offset: index + len(control_sequence)]
			offset = index + len(control_sequence)
			continue
		new_editorial += editorial[offset: index] + symbol
		offset = index + len(control_sequence)
	new_editorial += editorial[offset:]
	return new_editorial
			
def replace_latex(editorial: str) -> str:
	for character in latex_replace:
		editorial = replace_one(editorial, character[0], character[1])
	return editorial

if __name__ == '__main__':
	unicode_replace = [(character, unicode_replace[character]) for character in unicode_replace]
	unicode_replace = sorted(unicode_replace, key=lambda x: len(x[0]), reverse=True)
	latex_replace = [(character, latex_replace[character]) for character in latex_replace]
	latex_replace = sorted(latex_replace, key=lambda x: len(x[0]), reverse=True)
	names = get_problem_names()
	dataset = {
		'name': [],
		'description': [],
		'editorial': [],
		'tags': [],
		'rating': [],
		'source': [],
	}
	if True:
		for name in names:
			name = name[0]
			problem = get_problem(name)
			if '*special' in problem.tags:
				continue
			editorial = problem.editorial
			for character in unicode_replace:
				editorial = editorial.replace(character[0], character[1])
			editorial = replace_latex(editorial)
			problem.editorial = editorial
			dataset['name'].append(problem.name)
			dataset['description'].append(problem.description)
			dataset['editorial'].append(problem.editorial)
			dataset['tags'].append(', '.join(problem.tags) if problem.tags else '')
			dataset['rating'].append(str(problem.rating))
			dataset['source'].append(problem.source)
	if True:
		login(HF_WRITE_TOKEN)
		math_dataset_id = 'hendrycks/competition_math'
		math_dataset = datasets.load_dataset(math_dataset_id, split='train', trust_remote_code=True)
		for i, sample in enumerate(math_dataset):
			editorial = sample['solution']
			for character in unicode_replace:
				editorial = editorial.replace(character[0], character[1])
			editorial = replace_latex(editorial)
			dataset['name'].append(f'math_{i}')
			dataset['description'].append(sample['problem'])
			dataset['editorial'].append(editorial)
			dataset['tags'].append(sample['type'])
			dataset['rating'].append(sample['level'])
			dataset['source'].append('math')
	dataset_id = 'HoangLe1312/codecontest-reasoning'
	dataset = datasets.Dataset.from_dict(dataset)
	dataset.push_to_hub(dataset_id)
