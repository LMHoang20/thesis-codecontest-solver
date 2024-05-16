import helpers
import datasets
import nltk

from huggingface_hub import login
from database import get_db_conn
from entity.problem import Problem
from constants import *

needed_to_summarize = [
    "1008_E. Guess two numbers",
    "1023_G. Pisces",
    "1033_E. Hidden Bipartite Graph",
    "1033_F. Boolean Computer",
    "1033_G. Chip Game",
    "1044_A. The Tower is Going Home",
    "1044_B. Intersecting Subtrees",
    "1044_D. Deduction Queries",
    "1062_F. Upgrading Cities",
    "107_C. Arrangement",
    "107_E. Darts",
    "1080_D. Olya and magical square",
    "1091_G. New Year and the Factorisation Collaboration",
    "1118_F2. Tree Cutting (Hard Version)",
    "1153_E. Serval and Snake",
    "1163_F. Indecisive Taxi Fee",
    "1172_C2. Nauuo and Pictures (hard version)",
    "1174_F. Ehab and the Big Finale",
    "1178_H. Stock Exchange",
    "1185_G2. Playlist for Polycarp (hard version)",
    "1190_F. Tokitsukaze and Powers",
    "1205_C. Palindromic Paths",
    "1205_E. Expected Value Again",
    "1253_F. Cheap Robot",
    "1263_F. Economic Difficulties",
    "1279_F. New Year and Handle Change",
    "1293_D. Aroma's Search",
    "1304_F2. Animal Observation (hard version)",
    "1326_G. Spiderweb Trees",
    "1332_G. No Monotone Triples",
    "1355_F. Guess Divisors Count",
    "1359_C. Mixing Water",
    "1359_F. RC Kaboom Show",
    "1372_F. Omkar and Modes",
    "1375_H. Set Merging",
    "1375_I. Cubic Lattice",
    "1383_D. Rearrange",
    "1389_G. Directing Edges",
    "138_C. Mushroom Gnomes - 2",
    "1392_E. Omkar and Duck",
    "1392_F. Omkar and Landslide",
    "1392_G. Omkar and Pies",
    "1407_E. Egor in the Republic of Dagestan",
    "1420_E. Battle Lemmings",
    "1425_I. Impressive Harvesting of The Orchard",
    "1427_C. The Hard Work of Paparazzi",
    "1427_F. Boring Card Game",
    "1427_G. One Billion Shades of Grey",
    "1442_F. Differentiating Games",
    "1450_G. Communism",
    "1450_H2. Multithreading (Hard Version)",
    "1454_F. Array Partition",
    "1474_E. What Is It?",
    "1474_F. 1 2 3 4 ...",
    "1491_I. Ruler Of The Zoo",
    "1498_E. Two Houses",
    "1514_E. Baby Ehab's Hyper Apartment",
    "1517_H. Fly Around the World",
    "1521_C. Nastia and a Hidden Permutation",
    "1525_F. Goblins And Gnomes",
    "1526_F. Median Queries",
    "1534_E. Lost Array",
    "1539_E. Game with Cards",
    "1541_E1. Converging Array (Easy Version)",
    "1545_F. AquaMoon and Potatoes",
    "1550_F. Jumping Around",
    "226_E. Noble Knight's Path",
    "251_E. Tree and Table",
    "327_C. Magic Five",
    "327_E. Axis Walking",
    "340_E. Iahub and Permutations",
    "360_E. Levko and Game",
    "384_D. Volcanoes",
    "384_E. Propagating tree",
    "391_C3. The Tournament",
    "391_D2. Supercollider",
    "391_E2. Three Trees",
    "391_F1. Stock Trading",
    "391_F2. Stock Trading",
    "391_F3. Stock Trading",
    "430_C. Xor-tree",
    "471_E. MUH and Lots and Lots of Segments",
    "533_A. Berland Miners",
    "538_H. Summer Dichotomy",
    "549_E. Sasha Circle",
    "553_E. Kyoya and Train",
    "566_C. Logistical Questions",
    "611_G. New Year and Cake",
    "639_F. Bear and Chemistry",
    "671_E. Organizing a Race",
    "678_F. Lena and Queries",
    "710_F. String Set Queries",
    "724_G. Xor-matic Number of the Graph",
    "725_D. Contest Balloons",
    "758_C. Unfair Poll",
    "788_D. Finding lines",
    "807_D. Dynamic Problem Scoring",
    "853_D. Michael and Charging Stations",
    "917_A. The Monster",
    "950_F. Curfew",
    "991_F. Concise and clear"
]

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
	'\\frac12 ': '\\frac{1}{2}',
	'\\frac12': '\\frac{1}{2}',
	'\\&': '&',
	'\\%': '%',
	'\\#': '#',
	'\\_': '_',
}
latex_replace = {
	'\\leftrightarrow': '⇔',
	'\\Leftrightarrow': '⇔',
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
	'\\mathsf': '\\mathrm',
	'\\left': '',
	'\\right': '',
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

def get_problem_editorial(name):
	print(name)
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name, p.description, p.cf_tags, p.cf_rating, e.content
	FROM problems p
	JOIN editorials e ON p.name = e.name
	WHERE p.name = %s
	""", (name,))
	problem = cursor.fetchone()
	cursor.close()
	editorial = problem[4]
	while '<REMOVE-THIS>' in editorial:
		remove_start = editorial.find('<REMOVE-THIS>')
		remove_end = editorial.find('</REMOVE-THIS>') + len('</REMOVE-THIS>')
		editorial = editorial[:remove_start] + editorial[remove_end:]
	# editorial = remove_unescaped_dollars(editorial)
	return Problem(name=problem[0], description=problem[1], editorial=editorial, code='', tags=problem[2], rating=problem[3], source='codeforces')

def get_problem_editorial_summary(name):
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
	# problem_understanding = problem[4]
	solution_reasoning: str = problem[5]
	implementation_planning: str = problem[6]
	lines = []
	for line in solution_reasoning.split('\n'):
		if 'REASON:' in line:
			line = line.split('REASON:')[0].rstrip()
		if len(line.strip()) < 2:
			continue
		if line.lstrip().startswith('- '):
			if line.startswith('- '):
				line = line[2:].strip('*').strip('"')
			else:
				line = line[:line.index('-')] + line[line.index('-') + 2:].strip('*').strip('"')
			if not line.endswith('.'):
				line += '.'
			lines.append(line)
		else:
			raise Exception(f"Unexpected line: {line}")
	lines.append('We have the following plan to solve the problem:')
	for line in implementation_planning.split('\n'):
		if 'REASON:' in line:
			line = line.split('REASON:')[0].rstrip()
		if len(line.strip()) < 2:
			continue
		if line.lstrip().startswith('- '):
			if line.startswith('- '):
				line = line[2:].strip('*').strip('"')
			else:
				line = line[:line.index('-')] + line[line.index('-') + 2:].strip('*').strip('"')
			if not line.endswith('.'):
				line += '.'
			lines.append(line)
		else:
			if line == '// END OF ANSWER':
				continue
			if line == '// END OF SOLUTION':
				continue
			raise Exception(f"Unexpected line: {line}")
	editorial = '\n'.join(lines)
	editorial = helpers.remove_consecutive_line_breaks(editorial)
	# editorial = remove_unescaped_dollars(editorial)
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

def isalpha(char: str) -> bool:
	return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

def replace_one(editorial: str, control_sequence: str, symbol: str) -> str:
	editorial += ' '
	new_editorial = ''
	offset = 0
	while control_sequence in editorial[offset:]:
		index = editorial.index(control_sequence, offset)
		if escaped(editorial, index):
			new_editorial += editorial[offset: index + len(control_sequence)]
			offset = index + len(control_sequence)
			continue
		if isalpha(editorial[index + len(control_sequence)]):
			new_editorial += editorial[offset: index + len(control_sequence)]
			offset = index + len(control_sequence)
			continue
		if index - 1 >= 0 and editorial[index - 1] == ' ':
			new_editorial += editorial[offset: index - 1] + symbol
		else:
			new_editorial += editorial[offset: index] + symbol
		offset = index + len(control_sequence)
		if editorial[offset] == ' ':
			offset += 1
	new_editorial += editorial[offset:]
	return new_editorial.rstrip()
			
def replace_latex(editorial: str) -> str:
	for character in latex_replace:
		editorial = replace_one(editorial, character[0], character[1])
	return editorial

skip = [
	'393_B. Three matrices',
	'245_A. System Administrator',
	'630_A. Again Twenty Five!',
	'1080_B. Margarite and the best present',
	'1208_A. XORinacci',
	'1354_A. Alarm Clock',
	'1388_B. Captain Flint and a Long Voyage',
	'950_B. Intercepted Message',
	'1132_A. Regular Bracket Sequence',
	'1288_B. Yet Another Meme Problem',
	'869_B. The Eternal Immortality',
	'1345_B. Card Constructions',
	'1028_B. Unnatural Conditions',
	'1217_A. Creating a Character',
	'70_A. Cookies',
	'1420_C1. Pokémon Army (easy version)',
	'509_B. Painting Pebbles',
	'630_N. Forecast',
	'1513_B. AND Sequences',
	'1350_B. Orac and Models',
	'650_A. Watchmen',
	'1453_B. Suffix Operations',
	'1421_C. Palindromifier',
	'456_C. Boredom',
	# '825_D. Suitable Replacement'
]	

def create_table_line_separated_editorials():
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	CREATE TABLE line_separated_editorials (
		name VARCHAR(255) PRIMARY KEY,
		editorial TEXT
	)
	""")
	conn.commit()
	cursor.close()

def insert_line_separated_editorial_table(name: str, editorial: str):
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	INSERT INTO line_separated_editorials (name, editorial)
	VALUES (%s, %s)
	""", (name, editorial))
	conn.commit()
	cursor.close()

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
	create_table_line_separated_editorials()
	if True:
		for name in names:
			name = name[0]
			problem = get_problem_editorial(name)
			if '*special' in problem.tags:
				continue
			editorial = problem.editorial
			if '```' in editorial or problem.name in needed_to_summarize:
				editorial = get_problem_editorial_summary(name).editorial
				for character in unicode_replace:
					editorial = editorial.replace(character[0], character[1])
				editorial = editorial.replace('`', '').replace('****', '').replace('***', '').replace('**', '').replace(':\n$', ': $').replace('$\n', '$.\n')
				editorial = replace_latex(editorial)
				editorial = remove_unescaped_dollars(editorial)
			else:
				for character in unicode_replace:
					editorial = editorial.replace(character[0], character[1])
				editorial = editorial.replace('`', '').replace('****', '').replace('***', '').replace('**', '').replace(':\n$', ': $').replace('$\n', '$.\n')
				editorial = replace_latex(editorial)
				editorial = remove_unescaped_dollars(editorial)
				lines = editorial.split('\n')
				lines = [line.rstrip() for line in lines]
				lines = [line + '.' if line and (isalpha(line[-1]) or line[-1].isnumeric())  else line for line in lines]
				editorial = '\n'.join(lines)
				sent_text = nltk.sent_tokenize(editorial)
				sent_text = filter(lambda x: any(c.isalpha() for c in x), sent_text)
				sent_text = list(sent_text)
				sep = '\n'
				editorial = sep.join(sent_text)
				editorial = remove_unescaped_dollars(editorial)
				editorial = editorial.replace(f"i.e.{sep}", "i.e. ")
				if problem.name == '825_D. Suitable Replacement':
					editorial = editorial.replace(f"'?'{sep}", "'?' ")
			problem.editorial = editorial
			insert_line_separated_editorial_table(problem.name, editorial)
			dataset['name'].append(problem.name)
			dataset['description'].append(problem.description)
			dataset['editorial'].append(problem.editorial)
			dataset['tags'].append(', '.join(problem.tags) if problem.tags else '')
			dataset['rating'].append(str(problem.rating))
			dataset['source'].append(problem.source)
	if False:
		login(HF_WRITE_TOKEN)
		math_dataset_id = 'hendrycks/competition_math'
		math_dataset = datasets.load_dataset(math_dataset_id, split='train', trust_remote_code=True)
		for i, sample in enumerate(math_dataset):
			editorial = sample['solution']
			for character in unicode_replace:
				editorial = editorial.replace(character[0], character[1])
			editorial = replace_latex(editorial)
			sent_text = nltk.sent_tokenize(editorial)
			sent_text = filter(lambda x: any(c.isalpha() for c in x), sent_text)
			sent_text = list(sent_text)
			sep = '\n'
			editorial = sep.join(sent_text)
			dataset['name'].append(f'math_{i}')
			dataset['description'].append(sample['problem'])
			dataset['editorial'].append(editorial)
			dataset['tags'].append(sample['type'])
			dataset['rating'].append(sample['level'])
			dataset['source'].append('math')
	if True:
		dataset_id = 'HoangLe1312/raw-codecontest-reasoning'
		dataset = datasets.Dataset.from_dict(dataset)
		dataset.push_to_hub(dataset_id)
