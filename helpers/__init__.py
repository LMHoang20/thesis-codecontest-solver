from datetime import datetime
import nltk

def remove_consecutive_line_breaks(text):
	while '\n\n' in text:
		text = text.replace('\n\n', '\n')
	return text

def get_session_id():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

const_unicode_replace = {
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

const_latex_replace = {
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

unicode_replace = [(character, const_unicode_replace[character]) for character in const_unicode_replace]
unicode_replace = sorted(unicode_replace, key=lambda x: len(x[0]), reverse=True)
latex_replace = [(character, const_latex_replace[character]) for character in const_latex_replace]
latex_replace = sorted(latex_replace, key=lambda x: len(x[0]), reverse=True)

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

def normalize_editorial(editorial):
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
	editorial = editorial.replace(f"'?'{sep}", "'?' ")
	return editorial