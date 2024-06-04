import entity.problem

from database import get_db_conn

class Repository:
    def __init__(self) -> None:
        pass
    def insert(self, rows):
        pass
    def get(self):
        pass

class HuggingFace(Repository):
    def __init__(self, dataset_id, token=None) -> None:
        self.dataset_id = dataset_id
        self.token = token
    def insert(self, rows):
        pass
    def get(self):
        pass

class Problem(Repository):
    # constructor
    def __init__(self, connection) -> None:
        self.connection = connection
    # destructor
    def __del__(self):
        self.connection.close()
    def get_problem_names_with_editorials(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name, cf_contest_id, cf_index
            FROM problems p JOIN editorials e ON p.name = e.name
        """)
        problems = cursor.fetchall()
        cursor.close()
        return problems
    def get_problem(self, name: str) -> entity.problem.Problem:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
            FROM problems
            WHERE name = %s
        """, (name,))
        problem = cursor.fetchone()
        cursor.close()
        if not problem:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
                FROM testing_problems
                WHERE name = %s
            """, (name,))
            problem = cursor.fetchone()
            cursor.close()
        return entity.problem.Problem(name=problem[0], description=problem[1], rating=problem[2], tags=problem[3], public_tests=problem[4], private_tests=problem[5], generated_tests=problem[6], contest_id=problem[7], problem_id=problem[8], source='codeforces')
    def get_test_problems(self, split = None):
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
            FROM testing_problems
            {'WHERE split = %s' if split else ''}
            ORDER BY cf_rating, name
        """, (split,))
        problems = cursor.fetchall()
        cursor.close()
        return problems
    def get_random_problem(self, split = None, max_rating = None):
        cursor = self.connection.cursor()
        if split != "train":
            cursor.execute(f"""
                SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
                FROM testing_problems
                {'WHERE cf_rating <= %s' if max_rating else ''} 
                ORDER BY RANDOM()
                LIMIT 1
            """, (max_rating,))
        else:
            cursor.execute(f"""
                SELECT name, description, cf_rating, cf_tags, public_tests, private_tests, generated_tests, cf_contest_id, cf_index
                FROM problems
                {'WHERE cf_rating <= %s' if max_rating else ''}
                ORDER BY RANDOM()
                LIMIT 1
            """, (max_rating,))
        problem = cursor.fetchone()
        cursor.close()
        return entity.problem.Problem(name=problem[0], description=problem[1], rating=problem[2], tags=problem[3], public_tests=problem[4], private_tests=problem[5], generated_tests=problem[6], contest_id=problem[7], problem_id=problem[8], source='codeforces')

class SolveAttempt(Repository):
    def __init__(self, connection, table) -> None:
        self.connection = connection
        self.table = table
    def insert(self, rows):
        pass
    def get(self):
        pass