import datasets
import constants
import helpers
import re

from typing import List
from huggingface_hub import login
from database import get_db_conn


def create_table_editorials():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS editorials;
        CREATE TABLE editorials (
            name TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            solutions TEXT[] NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def insert_editorial(name: str, content: str, solutions: List[str]):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO editorials (name, content, solutions)
        VALUES (%s, %s, %s)
    """, (name, content, solutions))
    conn.commit()
    conn.close()

def get_dataset_from_hf():
    login(constants.HF_READ_TOKEN)
    dataset = datasets.load_dataset(constants.EDITORIAL_DATASET, split='train', cache_dir='cache-editorial')
    return dataset

mdLinks = re.compile(r'\[(.+)\]\(((?:(?:/|//codeforces.com/)contest/\d+/submission/|http).+)\)')

if __name__ == '__main__':
    dataset = get_dataset_from_hf()
    print(dataset)
    create_table_editorials()
    for problem in dataset:
        contest = problem['contest']
        index = problem['index']
        name = problem['name']
        description = problem['description']
        tags = problem['tags']
        sections = problem['editorial'].split('# TUTORIAL CODE XXX')
        assert len(sections) > 0
        editorial = sections[0].strip()
        if '[[Tutorial] Slope Trick]' in editorial:
            assert editorial.count('[[Tutorial] Slope Trick]') == 1
            # print(name)
            editorial = editorial.replace('[[Tutorial] Slope Trick]', '[Slope Trick]') 
        lines = editorial.split('\n')
        first_line = lines[0].strip()
        if mdLinks.search(editorial):
            for line in lines:
                if 'espresso.codeforces' in line or mdLinks.search(line):
                    with open('lines.md', 'r') as f:
                        content = f.read()
                    assert f'<{name}>' in content and f'</{name}>' in content
                    line = line.strip()
                    # print(name)
                    if name == '391_C1. The Tournament' or name == '391_C2. The Tournament':
                        new_name = '391_C3. The Tournament'
                    else:
                        new_name = name
                    original_start = content.index(line.strip())
                    original_end = original_start + len(line)
                    section_start = content.rindex(f'<{new_name}>', 0, original_start)
                    section_end = content.index(f'</{new_name}>', section_start)
                    fixed_start = content.index(f'<fixed>', original_end, section_end) + len('<fixed>')
                    fixed_end = content.index(f'</fixed>', fixed_start, section_end)
                    assert fixed_start < fixed_end
                    assert fixed_start > original_end
                    assert fixed_end < section_end
                    fixed = content[fixed_start:fixed_end].strip()
                    fixed = fixed.replace('<remove>', '<REMOVE-THIS>')
                    fixed = fixed.replace('</remove>', '</REMOVE-THIS>')
                    # print(line, fixed, sep='\n')
                    editorial = editorial.replace(line, fixed)
        editorial = editorial.replace(' (REFERENCE)**', '**')
        lines = editorial.split('\n')
        lines = [line.rstrip() for line in lines]
        editorial = '\n'.join(lines)
        solutions = sections[1:]
        for solution in solutions:
            assert solution.strip().startswith('```')
            assert solution.strip().endswith('```')
        description = helpers.remove_consecutive_line_breaks(description)
        editorial = helpers.remove_consecutive_line_breaks(editorial)
        insert_editorial(name.strip(), editorial.strip(), solutions)

