from database import get_db_conn
from entity.problem import Problem

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

class SolveAttempt(Repository):
    def __init__(self, connection, table) -> None:
        self.connection = connection
        self.table = table
    def insert(self, rows):
        pass
    def get(self):
        pass