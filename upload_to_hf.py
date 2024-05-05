import helpers
import datasets

from huggingface_hub import login
from database import get_db_conn
from entity.problem import Problem
from constants import *

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
	conn = get_db_conn()
	cursor = conn.cursor()
	cursor.execute(
	"""
	SELECT p.name, p.description, e.content, e.solutions, p.public_tests, p.private_tests, p.generated_tests, cf_tags, cf_rating
	FROM problems p
	JOIN editorials e ON p.name = e.name
	WHERE p.name = %s
	""", (name,))
	problem = cursor.fetchone()
	cursor.close()
	if len(problem[3]) > 0:
		code = problem[3][0]
	else:
		code, language = get_match_code(name)
		if language in [1, 3]:
			code = f'```py\n{code}\n```'
		elif language in [2]:
			code = f'```cpp\n{code}\n```'
	return Problem(name=problem[0], description=problem[1], editorial=problem[2], code=code, public_tests=problem[4], private_tests=problem[5], generated_tests=problem[6], tags=problem[7], rating=problem[8], source='codeforces')

def get_problem_names():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT p.name
    FROM problems p
    JOIN editorials e ON p.name = e.name
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

control_sequences = []
character_replace = {
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
    '-  >': '\\to',
    '{i * }': '{i*}',
    '\\,': ' ',
    '\\;': ' ',
    '\\:': ' ',
    '\\!': ' ',
}

unicode_characters = set()

if __name__ == '__main__':
    login(HF_WRITE_TOKEN)
    character_replace = [(character, character_replace[character]) for character in character_replace]
    character_replace = sorted(character_replace, key=lambda x: len(x[0]), reverse=True)
    names = get_problem_names()
    dataset = {
        'name': [],
        'description': [],
        'editorial': [],
        'code': [],
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
            for character in character_replace:
                editorial = editorial.replace(character[0], character[1])   
            while '<REMOVE-THIS>' in editorial:
                remove_start = editorial.find('<REMOVE-THIS>')
                remove_end = editorial.find('</REMOVE-THIS>') + len('</REMOVE-THIS>')
                editorial = editorial[:remove_start] + editorial[remove_end:]
            editorial = helpers.remove_consecutive_line_breaks(editorial)
            problem.editorial = editorial
            assert type(problem.code) == str
            dataset['name'].append(problem.name)
            dataset['description'].append(problem.description)
            dataset['editorial'].append(problem.editorial)
            dataset['code'].append(problem.code)
            dataset['tags'].append(', '.join(problem.tags) if problem.tags else '')
            dataset['rating'].append(str(problem.rating))
            dataset['source'].append(problem.source)
    math_dataset_id = 'hendrycks/competition_math'
    math_dataset = datasets.load_dataset(math_dataset_id, split='train', trust_remote_code=True)
    for i, sample in enumerate(math_dataset):
        editorial = sample['solution']
        for character in character_replace:
            editorial = editorial.replace(character[0], character[1])
        dataset['name'].append(f'math_{i}')
        dataset['description'].append(sample['problem'])
        dataset['editorial'].append(editorial)
        dataset['code'].append('')
        dataset['tags'].append(sample['type'])
        dataset['rating'].append(sample['level'])
        dataset['source'].append('math')
    dataset_id = 'HoangLe1312/codecontest-prompt'
    dataset = datasets.Dataset.from_dict(dataset)
    dataset.push_to_hub(dataset_id)
