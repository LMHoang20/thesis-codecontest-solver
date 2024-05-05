

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

class Problems(Repository):
    def __init__(self, connection, table) -> None:
        self.connection = connection
        self.table = table
    def insert(self, rows):
        pass
    def get(self):
        pass

class SolveAttempts(Repository):
    def __init__(self, connection, table) -> None:
        self.connection = connection
        self.table = table
    def insert(self, rows):
        pass
    def get(self):
        pass