from typing import List

class Problem:
    def __init__(self, name, description, rating, tags, source, public_tests=None, private_tests=None, generated_tests=None, contest_id=None, problem_id=None, editorial=None, code=None):
        self.name = name
        self.description = description
        self.rating = rating
        self.tags = tags
        self.source = source
        self.public_tests = public_tests
        self.private_tests = private_tests
        self.generated_tests = generated_tests
        self.contest_id = contest_id
        self.problem_id = problem_id
        self.editorial = editorial
        self.code = code
    def __str__(self) -> str:
        return f"Problem(name={self.name}, description={self.description}, rating={self.rating}, tags={self.tags}, source={self.source}, public_tests={self.public_tests}, private_tests={self.private_tests}, generated_tests={self.generated_tests}, contest_id={self.contest_id}, problem_id={self.problem_id}, editorial={self.editorial}, code={self.code})"
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "rating": self.rating,
            "tags": self.tags,
            "source": self.source,
            "public_tests": self.public_tests,
            "private_tests": self.private_tests,
            "generated_tests": self.generated_tests,
            "contest_id": self.contest_id,
            "problem_id": self.problem_id,
            "editorial": self.editorial,
            "code": self.code
        }
    def get_tests(self, public=True, private=True, generated=True) -> List[str]:
        tests = []
        if public:
            tests += [(test_input, test_output) for (test_input, test_output) in zip(self.public_tests['input'], self.public_tests['output'])]
        if private:
            tests += [(test_input, test_output) for (test_input, test_output) in zip(self.private_tests['input'], self.private_tests['output'])]
        if generated:
            tests += [(test_input, test_output) for (test_input, test_output) in zip(self.generated_tests['input'], self.generated_tests['output'])]
        return tests

