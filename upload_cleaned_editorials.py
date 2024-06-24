from database import get_db_conn
from repository import Problem
from helpers import escaped, isalpha, remove_consecutive_line_breaks
from transformers import AutoTokenizer
from huggingface_hub import login
from constants import HF_WRITE_TOKEN
from datasets import Dataset

model_id = "unsloth/Phi-3-medium-4k-instruct-bnb-4bit"
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="cache-phi-tokenizer")

def create_cleaned_editorials():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE cleaned_editorials (
            name TEXT PRIMARY KEY,
            description TEXT,
            editorial TEXT,
            solutions TEXT[],
            split TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_cleaned_editorial(name, description, editorial, solutions, split):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cleaned_editorials (name, description, editorial, solutions, split)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE SET
        description = EXCLUDED.description,
        editorial = EXCLUDED.editorial,
        solutions = EXCLUDED.solutions,
        split = EXCLUDED.split
    """, (name, description, editorial, solutions, split))
    conn.commit()
    cursor.close()
    conn.close()

def format_prompt(name, tags, rating, description, editorial):
    if type(tags) == list:
        tags = ', '.join(tags)
    assert type(tags) == str
    user_prompt = f"""
You are a Legendary Grandmaster competitive programmer on Codeforces.
You are given a competitive programming problem to solve.
Write the solution in natural language for the following problem.
You must start by predicting the topic of the problem and its rating.
The solution must be a detailed step-by-step, correct, and easy-to-understand guide to solve the problem.
Name: {name}
Description: {description}
"""
    model_answer = f"""
Topic: {tags}
Rating: {rating}
Solution:
{editorial}
"""
    prompt = tokenizer.apply_chat_template([
        {"role": "user", "content": user_prompt.strip()},
        {"role": "assistant", "content": model_answer.strip()}
    ], tokenize = False, add_generation_prompt = False)
    if not prompt.endswith(tokenizer.eos_token):
        prompt += tokenizer.eos_token
    token_count = tokenizer(prompt, return_length = True)['length']
    return prompt, token_count[0]

def in_math(text, index):
    cnt = 0
    for i in range(0, index):
        if text[i] != '$':
            continue
        if escaped(text, i):
            continue
        cnt += 1
    return cnt % 2 == 1

def remove_double_spaces_in_math(text):
    result = ''
    open_math = False
    for i in range(0, len(text)):
        if text[i] == '$' and not escaped(text, i):
            open_math = not open_math
        if not open_math:
            result += text[i]
            continue
        if text[i] != ' ':
            result += text[i]
            continue
        if i + 1 >= len(text):
            result += text[i]
            continue
        if text[i + 1] == ' ':
            continue
        result += text[i]
    return result

def find_control_sequences(text):
    control_sequences = []
    open_math = False
    for i in range(0, len(text)):
        if text[i] == '$' and not escaped(text, i):
            open_math = not open_math
        if not open_math:
            continue
        if text[i] != '\\':
            continue
        if i + 1 >= len(text):
            continue
        j = i + 1
        while j < len(text) and isalpha(text[j]):
            j += 1
        control_sequences.append(text[i:j])
    return control_sequences

def get_name(contest, problem):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM testing_problems
        WHERE cf_contest_id = %s AND cf_index = %s
    """, (contest, problem))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result is not None else None

def get_editorials():
    import os
    result = []
    for _, dirs, _ in os.walk('data/test_set'):
        for dir in dirs:
            for _, _, files in os.walk(f'data/test_set/{dir}'):
                for file in files:
                    if 'editorial' in file:
                        continue
                    assert file.endswith('.md')
                    file = file[:-3]
                    name = get_name(dir, file)
                    if name is None:
                        # print(f"Problem {dir}/{file} not found in the database")
                        continue
                    with open(f'data/test_set/{dir}/{file}.md', 'r') as f:
                        editorial = f.read()
                        if '$th' in editorial:
                            print(name)
                        lines = editorial.split('\n')
                        lines = lines[1:]
                        lines = [line.rstrip() for line in lines]
                        editorial = '\n'.join(lines).strip()
                    if '# TUTORIAL CODE XXX' in editorial:
                        code = editorial[editorial.index('# TUTORIAL CODE XXX') + len('# TUTORIAL CODE XXX'):]
                        editorial = editorial[:editorial.index('# TUTORIAL CODE XXX')].strip()
                    else:
                        code = ""
                    result.append((name, editorial, [code], 'test'))
    return result

    # conn = get_db_conn()
    # cursor = conn.cursor()
    # cursor.execute("""
    #     SELECT name, editorial, solutions, split
    #     FROM editorials_raw
    # """)
    # result = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # return result

def main():
    unicodes = {
        '\u200b': ' ',
        '\u2002': ' ',
        '\xa0': ' ',
        '\u2009': ' ',
        '–': '-',
        '−': '-',
        '—': '-',
        '，': ', ',
        '’': "'",
        '‘': "'",
        '”': "'",
        '“': "'",
        '′': "'",
        'ö': 'o',
        '…': '...',
        'С': 'C',
    }
    unicodes_in_math = {
        '≤': '\\leq',
        'П': '\\Pi',
        '»': '\\gg',
        '→': '\\implies',
        '⌈': '\\lceil',
        'Ω': '\\Omega',
        'а': '\\alpha',
        'ε': '\\varepsilon',
        '∈': '\\in',
        '×': '\\times',
        '⌊': '\\lfloor',
        '⌉': '\\rceil',
        '⋅': '\\cdot',
        '∞': '\\infty',
        '≥': '\\geq',
        '•': '\\cdot',
        'α': '\\alpha', 
        '·': '\\cdot',
        '≠': '\\neq',
        'Σ': '\\Sigma',
        '≈': '\\approx',
        'Δ': '\\Delta',
        '«': '\\ll',
        '⌋': '\\rfloor',
        'π': '\\pi',
        '←': '\\gets',
        '±': '\\pm',
        'φ': '\\phi',
        '↔': '\\iff',
        '≡': '\\equiv',
        'ρ': '\\rho',
    }
    normalize_control_sequences = {
        # remove
        '\\Big': '',
        '\\big': '',
        '\\displaystyle': '',
        '\\left': '',
        '\\quad': '',
        '\\right': '',
        '\\limits': '',
        '\\newline': '',
        '\\': '',
        # normalize
        '\\leftarrow': '\\gets',
        '\\rightarrow': '\\to',
        '\\argmin': '\\argmin',
        '\\max': '\\max',
        '\\ln': '\\ln',
        '\\mod': '\\bmod',
        '\\sin': '\\sin',
        '\\frac': '\\dfrac',
        '\\cdot': '\\times',
        '\\gcd': '\\gcd',
        '\\arccos': '\\arccos',
        '\\cos': '\\cos',
        '\\det': '\\det',
        '\\blacksquare': '\\square',
        '\\varepsilon': '\\epsilon',
        '\\geqslant': '\\ge',
        '\\leqslant': '\\le',
        '\\backslash': '\\setminus',
        '\\leftrightarrow': '\\iff',
        '\\Rightarrow': '\\implies',
        '\\lbrace': '\\{',
        '\\mid': '|',
        '\\nmid': '\\not |',
        '\\vert': '|',
        '\\rbrace': '\\}',
        '\\neq': '\\ne',
        '\\geq': '\\ge',
        '\\leq': '\\le',
        '\\bigcup': '\\cup',
        '\\varnothing': '\\emptyset',
        '\\lt': '<',
        '\\gt': '>',
        '\\cdots': '...',
        '\\ldots': '...',
        '\\dots': '...',
        '\\empty': '\\emptyset',
        '\\overrightarrow': '\\vec',
        '\\vee': '\\lor',
        '\\wedge': '\\land',
        '\\varphi': '\\phi',
        '\\vdots': '|',
        '\\sim': '\\approx',
        # special
        '\\mathcal O': 'O',
        '\\mathcal{O}': 'O',
        '\\mathrm': '\\text',
        '\\mathbb': '\\text',
        '\\textbf': '\\text',
    }

    problem_repo = Problem(get_db_conn())
    # create_cleaned_editorials()
    editorials = get_editorials()

    train_prompts = []
    train_token_counts = []
    validation_prompts = []
    validation_token_counts = []
    unicodes_in_math = [(k, v) for k, v in unicodes_in_math.items()]
    unicodes_in_math = sorted(unicodes_in_math, key=lambda x: len(x[0]), reverse=True)

    control_sequences = [(k, v) for k, v in normalize_control_sequences.items()]
    control_sequences = sorted(control_sequences, key=lambda x: (len(x[0]), len(x[1])), reverse=True)

    css = set()
    for name, editorial, solutions, split in editorials:
        assert split == 'train' or split == 'validate' or split == 'test'
        original = editorial
        while '<REMOVE-THIS>' in editorial:
            start = editorial.index('<REMOVE-THIS>')
            end = editorial.index('</REMOVE-THIS>')
            editorial = editorial[:start] + editorial[end + len('</REMOVE-THIS>'):]
        for unicode, replacement in unicodes.items():
            editorial = editorial.replace(unicode, replacement)
        for char, replacement in unicodes_in_math:
            offset = 0
            while char in editorial[offset:]:
                index = editorial.index(char, offset)
                if in_math(editorial, index):
                    if index + len(char) < len(editorial) and editorial[index + len(char)] != ' ':
                        editorial = editorial[:index] + replacement + ' ' + editorial[index + len(char):]
                        offset = index + len(replacement) + 1
                    else:
                        editorial = editorial[:index] + replacement + editorial[index + len(char):]
                        offset = index + len(replacement)
                else:
                    offset = index + len(char)
        for control_sequence, replacement in control_sequences:
            offset = 0
            while control_sequence in editorial[offset:]:
                index = editorial.index(control_sequence, offset)
                if in_math(editorial, index) and not isalpha(editorial[index + len(control_sequence)]):
                    editorial = editorial[:index] + replacement + editorial[index + len(control_sequence):]
                    offset = index + len(replacement)
                else:
                    offset = index + len(control_sequence)
        editorial = remove_double_spaces_in_math(editorial)
        editorial = remove_consecutive_line_breaks(editorial)
        problem = problem_repo.get_problem(name)
        assert problem is not None
        problem.description = remove_double_spaces_in_math(problem.description)
        problem.description = remove_consecutive_line_breaks(problem.description)
        assert split == 'test'
        insert_cleaned_editorial(name, problem.description, editorial, solutions, split)
        css |= set(find_control_sequences(editorial))
        # prompt, token_count = format_prompt(problem.name, problem.tags, problem.rating, problem.description, editorial)
        # if split == 'train':
        #     train_prompts.append(prompt)
        #     train_token_counts.append(token_count)
        # elif split == 'validate':
        #     validation_prompts.append(prompt)
        #     validation_token_counts.append(token_count)
    # login(HF_WRITE_TOKEN)
    # train_split = Dataset.from_dict({'prompt': train_prompts, 'token_count': train_token_counts})
    # train_split.push_to_hub("HoangLe1312/codecontest-prompts", split = 'train')
    # validation_split = Dataset.from_dict({'prompt': validation_prompts, 'token_count': validation_token_counts})
    # validation_split.push_to_hub("HoangLe1312/codecontest-prompts", split = 'validate')
    # total_train_token_count = sum(train_token_counts)
    # total_validation_token_count = sum(validation_token_counts)
    # if any(token_count > 4096 for token_count in train_token_counts):
    #     print("Train token count exceeds 4096")
    # if any(token_count > 4096 for token_count in validation_token_counts):
    #     print("Validate token count exceeds 4096")
    # print(f"Total train token count: {total_train_token_count}")
    # print(f"Total validation token count: {total_validation_token_count}")
    print(css)
if __name__ == '__main__':
    main()