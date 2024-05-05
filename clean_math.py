import re

from database import get_db_conn

def get_editorial(name):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT content
        FROM editorials
        WHERE name = %s
    """, (name,))
    editorial = cursor.fetchone()
    cursor.close()
    conn.close()
    return editorial[0]

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
}
unicode_characters = set()

if __name__ == '__main__':
    character_replace = [(character, character_replace[character]) for character in character_replace]
    character_replace = sorted(character_replace, key=lambda x: len(x[0]), reverse=True)
    names = get_problem_names()
    for name in names:
        name = name[0]
        editorial = get_editorial(name)
        for character in character_replace:
            editorial = editorial.replace(character[0], character[1])
        dollar_start = -1
        unicodes = re.sub(r"[\x00-\x7f]+", "", editorial) 
        if len(unicodes) > 0:
            for character in unicodes:
                unicode_characters.add((character, ord(character)))
        if True:
            for i in range(len(editorial)):
                if editorial[i] == '$':
                    if not escaped(editorial, i):
                        if dollar_start == -1:
                            dollar_start = i
                        else:
                            math = editorial[dollar_start + 1:i]
                            dollar_start = -1
                            math_offset = 0
                            while '\\' in math[math_offset:]:
                                sequence_start = math.find('\\', math_offset)
                                if escaped(math, sequence_start):
                                    math_offset = sequence_start + 1
                                    continue
                                for j in range(sequence_start + 1, len(math)):
                                    if not math[j].isalpha():
                                        sequence = math[sequence_start:j]
                                        control_sequences.append(sequence)
                                        break
                                math_offset = sequence_start + 1
    for character in unicode_characters:
        print(character)
    
    sequences = list(set(control_sequences))
    sequences = sorted(sequences, key=lambda x: len(x), reverse=True)
    for sequence in sequences:
        print(sequence)
    
                            
                    
        