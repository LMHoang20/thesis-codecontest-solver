import os

from database import get_db_conn

def create_table_editorials_raw():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS editorials_raw;
        CREATE TABLE IF NOT EXISTS editorials_raw (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            editorial TEXT NOT NULL,
            solutions TEXT[] NOT NULL,
            split TEXT NOT NULL,
            note TEXT DEFAULT NULL
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()

def check_exists(name, table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * 
        FROM {table}
        WHERE name = %s
        """, (name,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_name(contest_id, problem_id, table='problems'):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT name
        FROM {table}
        WHERE cf_contest_id = %s AND cf_index = %s
        """, (contest_id, problem_id)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result is not None else ''

def insert_editorial(table, name, editorial, solutions, split, note):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        INSERT INTO {table} (name, editorial, solutions, split, note)
        VALUES (%s, %s, %s, %s, %s)
        """, (name, editorial, solutions, split, note)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_solutions_from_V1(name):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT solutions
        FROM editorials
        WHERE name = %s
        """, (name,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result is not None else []

def get_match_code(name):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT code, language
    FROM matches_v2
    WHERE name = %s
    AND score = 5
    ORDER BY session_id DESC
    """, (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return f'```{result[1]}\n{result[0]}\n```'
    
editorials = {}
    
splitter = '# TUTORIAL CODE XXX'

def handle_1(root, file, split):
    contest_id = root.split('/')[-1]
    problem_id = file.split('.')[0]
    name = get_name(contest_id, problem_id)
    if name == '':
        return
    if check_exists(name, 'editorials_raw'):
        return
    path = f'{root}/{file}'
    print(contest_id, problem_id)
    with open(f'{root}/{file}', 'r') as f:
        lines = f.readlines()
        editorial = ''.join(lines[1:]).strip()
        if splitter in editorial:
            sections = editorial.split(splitter)
            editorial = sections[0]
            solutions = sections[1:]
            for solution in solutions:
                assert solution.strip().startswith('```') and solution.strip().endswith('```'), path
            solutions = [solution.strip() for solution in solutions]
            insert_editorial('editorials_raw', name, editorial, solutions, split, 'from extra self')
        else:
            insert_editorial('editorials_raw', name, editorial, [get_match_code(name)], split, 'from extra, match code')
    

splitter_2 = 'TUTORIAL CODE XXX'

def handle_2(root, file, split):
    contest_id, problem_id, _ = file.split('-')
    name = get_name(contest_id, problem_id)
    if name == '':
        return
    if check_exists(name, 'editorials_raw'):
        return
    path = f'{root}/{file}'
    print(contest_id, problem_id)
    with open(f'{root}/{file}', 'r') as f:
        lines = f.readlines()
        editorial = ''.join(lines[1:]).strip()
        if splitter_2 in editorial:
            sections = editorial.split(splitter_2)
            editorial = sections[0]
            solutions = sections[1:]
            for solution in solutions:
                assert solution.strip().startswith('```') and solution.strip().endswith('```'), path
            solutions = [solution.strip() for solution in solutions]
            insert_editorial('editorials_raw', name, editorial, solutions, split, 'from extra QL')
        else:
            insert_editorial('editorials_raw', name, editorial, [get_match_code(name)], split, 'from extra QL, match code')
    

def handle_3(root, file, split):
    contest_id, problem_id, _ = file.split('-')
    if contest_id == '409' or contest_id == '391':
        return
    name = get_name(contest_id, problem_id)
    if name == '':
        return
    if check_exists(name, 'editorials_raw'):
        return
    path = f'{root}/{file}'
    print(contest_id, problem_id)
    with open(f'{root}/{file}', 'r') as f:
        editorial = f.read()
        if splitter in editorial:
            sections = editorial.split(splitter)
            editorial = sections[0]
            new_solutions = sections[1:]
            for solution in new_solutions:
                assert (solution.strip().startswith('```cpp\n') or solution.startswith('```py\n')) and solution.strip().endswith('```'), path
            new_solutions = [solution.strip() for solution in new_solutions]
        else:
            new_solutions = []
        translated_solutions = []
        if os.path.exists(f'translated/{name}.cpp'):
            with open(f'translated/{name}.cpp', 'r') as f:
                content = f.read().strip()
                if not content.startswith('```cpp'):
                    content = f'```cpp\n{content}\n```'
                assert not content.startswith('```cpp\n```cpp\n')
                translated_solutions.append(content)
        if os.path.exists(f'translated/{name}.py'):
            with open(f'translated/{name}.py', 'r') as f:
                content = f.read().strip()
                content = f'```py\n{content}\n```'
                translated_solutions.append(content)
        existing_solutions = get_solutions_from_V1(name)
        solutions = new_solutions + translated_solutions + existing_solutions 
        solutions = [solution.strip() for solution in solutions if solution.strip() != '']
        if len(solutions) == 0:
            insert_editorial('editorials_raw', name, editorial, [get_match_code(name)], split, 'from corrected, match code')
        else:
            insert_editorial('editorials_raw', name, editorial, solutions, split, 'from corrected')

def handle_4(root, file, split):
    contest_id = root.split('/')[-1]
    problem_id = file.split('.')[0]
    print(contest_id, problem_id)
    name = get_name(contest_id, problem_id, 'testing_problems')
    if name == '':
        print(f'{root}/{file}')
        return
    if check_exists(name, 'editorials_raw'):
        return
    path = f'{root}/{file}'
    print(contest_id, problem_id)
    with open(f'{root}/{file}', 'r') as f:
        lines = f.readlines()
        editorial = ''.join(lines[1:]).strip()
        if splitter in editorial:
            sections = editorial.split(splitter)
            editorial = sections[0]
            solutions = sections[1:]
            for solution in solutions:
                assert solution.strip().startswith('```') and solution.strip().endswith('```'), path
            solutions = [solution.strip() for solution in solutions]
        else:
            solutions = []
        if len(solutions) == 0:
            insert_editorial('editorials_raw', name, editorial, [get_match_code(name)], split, 'from validation, match code')
        else:
            insert_editorial('editorials_raw', name, editorial, solutions, split, 'from validation')

def main():
    create_table_editorials_raw()
    print('from extra')
    for root, _, files in os.walk('data/contests-extra'):
        if 'skip' in root:
            continue
        if 'generated' not in root:
            for file in files:
                if 'editorial' in file:
                    continue
                try:
                    handle_1(root, file, 'train')
                except Exception as e:
                    print(e)
    print('from corrected')
    for root, _, files in os.walk('data/corrected'):
        for file in files:
            if 'reviewed' not in file:
                continue
            assert len(file.split('-')) == 3
            contest_id, problem_id, _ = file.split('-')
            path = f'{root}/{file}'
            with open(path, 'r') as f:
                content = f.read()
                if content.strip() == '':
                    continue
            from_extra = False
            if os.path.exists(f'data/contests-extra/{contest_id}_generated'):
                assert not os.path.exists(f'data/corrected/{contest_id}-{problem_id}.md') and \
                    not os.path.exists(f'data/corrected/{contest_id}-{problem_id}-corrected.md') and \
                    not os.path.exists(f'data/corrected/{contest_id}-{problem_id}-corrected-gemini.md')
                from_extra = True
            if from_extra:
                try:
                    handle_2(root, file, 'train')
                except Exception as e:
                    print(e)
            else:
                try:
                    handle_3(root, file, 'train')
                except Exception as e:
                    print(e)
    print('from validation')
    for root, _, files in os.walk('data/validate_set'):
        for file in files:
            if 'editorial' in file:
                continue
            if 'skip' in file:
                continue
            try:
                handle_4(root, file, 'validate')
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()