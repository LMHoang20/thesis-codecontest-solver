import os

from database import get_db_conn

def create_table_editorials_v2():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        DROP TABLE IF EXISTS editorials_v2;
        CREATE TABLE IF NOT EXISTS editorials_v2 (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            editorial TEXT NOT NULL,
            solutions TEXT[] NOT NULL,
            notes TEXT NOT NULL,
            split TEXT NOT NULL,
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()

def check_exists(contest_id, problem_id, table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * 
        FROM {table}
        WHERE cf_contest_id = %s AND cf_index = %s
        """, (contest_id, problem_id)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def handle_corrected(dir, file):
    print(dir, file)

def handle_QL(dir, file):
    path = f'data/contests-extra/{dir}/{file}'
    print(path)
    with open(path, 'r') as f:
        lines = f.readlines()
        print(lines[0])
    
def handle(dir, file):
    print(dir, file)

for root, dirs, files in os.walk('data/contests-extra'):
    if 'skip' in root:
        continue
    files = [file for file in files if 'editorial' not in file]
    other_filtered = [file for file in files if '-skip' not in file and 'corrected' not in file]
    filtered = [file for file in files if 'corrected' in file]
    assert (len(other_filtered) == len(filtered)) or ('generated' not in root), (root, other_filtered, filtered)
    dir = root.split('/')[-1]
    if 'generated' in root:
        for file in filtered:
            handle_QL(dir, file)
            pass
    # else:
    #     for file in files:
    #         handle(dir, file)