import os
import yaml
import re
import unicodedata

from database import get_db_conn
from helpers import remove_consecutive_line_breaks, escaped, isalpha

normalize_control_sequences = {
    # remove
    '\\big': '',
    '\\displaystyle': '',
    '\\left': '',
    '\\quad': '',
    '\\right': '',
    '\\limits': '',
    '\\newline': '',
    '\\': '',
    '\\textstyle': '',
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
    '\\bigcap': '\\cap',
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
    '\\textbf': '\\text',
    '\\textit': '\\text',
    '\\texttt': '\\text',
}

def is_unicode(char):
    return ord(char) > 127

def strip_not_in_code(text):
    in_code = False
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if '```' in line:
            assert line.strip() == '```', line
            in_code = not in_code
        if not in_code:
            while lines[i].startswith('-  '):
                lines[i] = '- ' + lines[i][3:]
            if not lines[i].lstrip().startswith('-'):
                lines[i] = lines[i].strip()
                while '  ' in lines[i]:
                    lines[i] = lines[i].replace('  ', ' ')
        else:
            lines[i] = lines[i].rstrip()
    return '\n'.join(lines)

def remove_space_before_after_punctuation(text):
    punctuation_before = {',', '.', '?', '!', ':', ';', ')', ']', '}'}
    for p in punctuation_before:
        text = text.replace(f' {p}', p)
    punctuation_after = {'(', '[', '{'}
    for p in punctuation_after:
        text = text.replace(f'{p} ', p)
    return text
            
unicodes = set()

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

css = set()

def normalize_control_sequence(text):
    control_sequences = [(k, v) for k, v in normalize_control_sequences.items()]
    control_sequences = sorted(control_sequences, key=lambda x: (len(x[0]), len(x[1])), reverse=True)
    for control_sequence, replacement in control_sequences:
        offset = 0
        while control_sequence in text[offset:]:
            index = text.index(control_sequence, offset)
            if in_math(text, index) and not isalpha(text[index + len(control_sequence)]):
                text = text[:index] + replacement + text[index + len(control_sequence):]
                offset = index + len(replacement)
            else:
                offset = index + len(control_sequence)
    return text

def normalize_th(text):
    text = text.replace('$th', '$-th')
    text = text.replace('$st', '$-st')
    text = text.replace('$nd', '$-nd')
    text = text.replace('$rd', '$-rd')
    return text

def normalize(text):
    return normalize_th(
        remove_double_spaces_in_math(
            normalize_control_sequence(
                remove_space_before_after_punctuation(
                    remove_consecutive_line_breaks(
                        strip_not_in_code(text)
                    )
                )
            )
        )
    )

def insert_cleaned_editorial(name, description, editorial, solutions, split):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cleaned_editorials (name, description, editorial, solutions, split)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, description, editorial, solutions, split))
    conn.commit()
    cursor.close()
    conn.close()

for root, _, files in os.walk('data/new_gemini'):
    for file in files:
        assert file.endswith('.yaml')
        path = f'{root}/{file}'
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            assert len(data.keys()) == 5, path
            code, language = data['code'].strip(), data['language'].strip()
            if code == '':
                print(path)
            if language == 'python':
                language = 'py'
            code = f'```{language}\n{code}\n```'
            title, description, solution = data['title'].strip(), data['description'].strip(), data['solution'].strip()
            if description.startswith('Table:'):
                continue
            if any(is_unicode(char) for char in title):
                print(path)
                print(title)
                print('----------------')
            assert title != '', path
            assert description != '', path
            assert solution != '', path
            # if solution in description:
            #     print(path)
            if description.startswith('Formatted question'):
                # skip first line
                description = description[description.index('\n') + 1:]
            if 'Related Topics' in description:
                description = description[:description.index('Related Topics')]
                # print(path)
                # print(description)
                # print('---------------')
            if 'Companies' in description:
                description = description[:description.index('Companies')]
                # print(path)
                # print(description[description.index('Companies'):])
                # print('---------------')
            if 'Follow up' in description:
                description = description[:description.index('Follow up')]
                # print(path)
                # print(description[description.index('Follow up'):])
                # print('---------------')
            if 'Follow-up' in description:
                description = description[:description.index('Follow-up')]
                # print(path)
                # print(description[description.index('Follow-up'):])
                # print('---------------')
            # if title[title.index('.') + 1:].strip() in description:
            #     print(path)
            #     print(title[title.index('.') + 1:].strip())
            #     print(description)
            #     print('---------------')
            # if 'http' in solution:
            #     print(path)
            #     print(solution)
            #     print('---------------')
            # if 'class Solution' in solution:
            #     print(path)
            md_link_re = r'\[.*?\]\(.*?\)'
            md_links = re.findall(md_link_re, description)
            for md_link in md_links:
                placeholder = md_link.split(']')[0] + ']'
                url = md_link.split(']')[1][1:-1]
                # print(placeholder, url, path)
                assert f'{placeholder}({url})' == md_link, path
                placeholder = placeholder[1:-1].strip()
                assert description.count(md_link) == 1, path
                # replace the link with the placeholder, add space before and after the placeholder if not already there
                # print(description[description.index(md_link) - 1], description[description.index(md_link) + len(md_link)])
                has_space_before = description[description.index(md_link) - 1] == ' '
                has_space_after = description[description.index(md_link) + len(md_link)] == ' '
                if not has_space_before:
                    placeholder = ' ' + placeholder
                if not has_space_after:
                    placeholder = placeholder + ' '
                description = description.replace(md_link, placeholder)
            description = description.strip()
            solution = solution.strip()
            if solution.endswith('\n# Code'):
                solution = solution[:-7].strip()
            lines = solution.split('\n')
            if len(lines) == 1:
                continue
            description = unicodedata.normalize('NFKC', description)
            solution = unicodedata.normalize('NFKC', solution)
            # for char in description:
            #     if is_unicode(char):
            #         unicodes.add(char)
            # for char in solution:
            #     if is_unicode(char):
            #         unicodes.add(char)
            # print(description)
            # print('----------------')
            # print(solution)
            # print('================')
            description = description.replace('\u200b', '')
            description = description.replace('\\]', '\\]\n')
            description = normalize(description)
            solution = solution.replace('\u200b', '')
            solution = solution.replace('\\]', '\\]\n')
            solution = solution.replace('(LeetCode problem 155)', '')
            solution = normalize(solution)
            # insert_cleaned_editorial(title, description, solution, [code], 'leetcode')
            # print(description)
            # print('----------------')
            # print(solution)
            # print('================')
            # print(path)
            # css |= set(find_control_sequences(description))
            # css |= set(find_control_sequences(solution))
            # first_line = lines[0]
            # last_line = lines[-1]
            # if not last_line.startswith('The time complexity'):
            #     print(last_line, path)
            #     print('------------')
            if title.startswith('2788'):
                continue
            assert description.count('$') % 2 == 0, path
            assert solution.count('$') % 2 == 0, path
            assert description.count('`') % 2 == 0, path
            assert solution.count('`') % 2 == 0, path
