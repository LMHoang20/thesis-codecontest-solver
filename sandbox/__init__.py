import os
import subprocess

def compare_int(test_output, code_output):
    try:
        test = int(test_output)
        code = int(code_output)
        return (True, test != code)
    except ValueError:
        return (False, None)

def compare_float(test_output, code_output):
    try:
        test = float(test_output)
        code = float(code_output)
        return (True, abs(test - code) > 1e-6)
    except ValueError:
        return (False, None)
    
def compare_str(test_output, code_output, case_sensitive=False):
    if case_sensitive:
        return test_output != code_output
    return test_output.lower() != code_output.lower()

class Checker:
    def __init__(self) -> None:
        pass
    def check(self, test_input, test_output, code_output):
        test_output = test_output.strip().split()
        code_output = code_output.strip().split()
        if len(test_output) != len(code_output):
            return False
        for _ in range(len(test_output)):
            ok, result = compare_int(test_output, code_output)
            if not ok:
                ok, result = compare_float(test_output, code_output)
            if not ok:
                result = compare_str(test_output, code_output)
            if not result:
                return False
        return True

class Sandbox:
    def __init__(self, language, threadsafe) -> None:
        pass
    def run(self, code: str, test_input: str):
        pass

class PythonSandbox(Sandbox):
    def __init__(self, id) -> None:
        self.script_file = f'{id}.py'

    def run(self, code: str, test_input: str):
        with open(self.script_file, 'w') as f:
            f.write(code)
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
        self.executable_file = f'{id}'
        self.code_file = f'{id}.cpp'
    
    def compile(self, code: str):
        with open(self.code_file, 'w') as f:
            f.write(code)
        return subprocess.run(["g++", "-w", "-std=c++20", "-I", os.getcwd(), "-o", self.executable_file, self.code_file], capture_output=True).stderr.decode('utf-8')
    
    def run(self, test_input: str):
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
    def __init__(self, sandbox: Sandbox, checker: Checker, threadsafe=False) -> None:
        self.sandbox = sandbox
        self.checker = checker
    def judge_tests(self, tests):
        for test in tests:
            test_input, test_output = test
            try:
                result = self.sandbox.run(test_input)
                code_stdout = result['stdout']
                code_stderr = result['stderr']
            except subprocess.TimeoutExpired:
                return ("Time Limit Exceeded", test_input)
            except subprocess.CalledProcessError as e:
                return ("Runtime Error", e.stderr)
            except MemoryError:
                return ("Memory Limit Exceeded", test_input)
            if not self.checker.check(test_input, test_output, code_stdout):
                return ("Wrong Answer", test_input, test_output, code_stdout, code_stderr)
        return ("OK", len(tests))
