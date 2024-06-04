import os
import subprocess

from logger import Logger
from typing import List, Tuple

def compare_int(test_output, code_output):
    try:
        test = int(test_output)
        code = int(code_output)
        return (True, test == code)
    except Exception:
        return (False, None)

def compare_float(test_output, code_output):
    try:
        test = float(test_output)
        code = float(code_output)
        return (True, abs(test - code) < 1e-5)
    except Exception:
        return (False, None)
    
def compare_str(test_output: str, code_output: str, case_sensitive=False):
    if case_sensitive:
        return test_output == code_output
    return test_output.lower() == code_output.lower()

class Checker:
    def __init__(self) -> None:
        pass
    def check(self, test_input, test_output, code_output):
        test_output = test_output.strip().split()
        code_output = code_output.strip().split()
        if len(test_output) != len(code_output):
            return False, f'expected {len(test_output)} outputs but got {len(code_output)}'
        for i in range(len(test_output)):
            test_output[i] = test_output[i].strip()
            code_output[i] = code_output[i].strip()
            ok, result = compare_int(test_output[i], code_output[i])
            if not ok:
                ok, result = compare_float(test_output[i], code_output[i])
            if not ok:
                result = compare_str(test_output[i], code_output[i])
            if not result:
                return False, f'expected {test_output[i]} but got {code_output[i]}'
        return True, ''

class Sandbox:
    def __init__(self, id) -> None:
        pass
    def run(self, code: str, test_input: str):
        pass

GENERATED_FILE_PATH = 'judges'
if not os.path.exists(GENERATED_FILE_PATH):
    os.makedirs(GENERATED_FILE_PATH)

class PythonSandbox(Sandbox):
    def __init__(self, id) -> None:
        self.script_file = f'{GENERATED_FILE_PATH}/{id}.py'

    def run(self, code: str, test_input: str):
        with open(self.script_file, 'w') as f:
            f.write(code + '\n')
        try:
            result = subprocess.run(['timeout', '2s', 'python3', self.script_file], input=test_input, capture_output=True, text=True, timeout=5)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': 'Time Limit Exceeded',
                'stderr': ''
            }
        except subprocess.CalledProcessError as e:
            return {
                'stdout': 'Runtime Error',
                'stderr': e.stderr
            }
        except MemoryError:
            return {
                'stdout': 'Memory Limit Exceeded',
                'stderr': ''
            }
        

class CppSandbox(Sandbox):
    def __init__(self, id) -> None:
        self.executable_file = f'{GENERATED_FILE_PATH}/{id}'
        self.code_file = f'{GENERATED_FILE_PATH}/{id}.cpp'
    
    def compile(self, code: str) -> str:
        with open(self.code_file, 'w') as f:
            f.write(code + '\n')
        return subprocess.run(["g++", "-w", "-std=c++20", "-I", os.getcwd(), "-o", self.executable_file, self.code_file], capture_output=True).stderr.decode('utf-8')
    
    def run(self, code: str, test_input: str):
        compile_error = self.compile(code).strip()
        if compile_error != '':
            return {
                'stdout': 'Compilation',
                'stderr': compile_error
            }
        if not os.path.exists(f'./{self.executable_file}'):
            raise FileNotFoundError(f'{self.executable_file} not found')
        try:
            result = subprocess.run(['timeout', '2s', f'./{self.executable_file}'], input=test_input, capture_output=True, text=True, timeout=5)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': 'Time Limit Exceeded',
                'stderr': ''
            }
        except subprocess.CalledProcessError as e:
            return {
                'stdout': 'Runtime Error',
                'stderr': e.stderr
            }
        except MemoryError:
            return {
                'stdout': 'Memory Limit Exceeded',
                'stderr': ''
            }

class Judge:
    def __init__(self, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
    def judge_tests(self, problem_name: str, code: str, language: str, tests: List[Tuple[str, str]], checker: Checker=Checker()):
        if language == 'cpp':
            sandbox = CppSandbox(self.name)
        else:
            sandbox = PythonSandbox(self.name)
        for i, test in enumerate(tests):
            self.logger.info(problem_name,  "judging test", i+1, "out of", len(tests))
            test_input, test_output = test
            try:
                result = sandbox.run(code, test_input)
                code_stdout = result['stdout']
                code_stderr = result['stderr']
            except subprocess.TimeoutExpired:
                return ("Time Limit Exceeded", test_input)
            except subprocess.CalledProcessError as e:
                return ("Runtime Error", e.stderr)
            except MemoryError:
                return ("Memory Limit Exceeded", test_input)
            result, reason = checker.check(test_input, test_output, code_stdout)
            if not result:
                return ("Wrong Answer", test_input, test_output, code_stdout, code_stderr, reason)
        return ("OK", len(tests))
