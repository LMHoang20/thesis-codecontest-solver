import subprocess

executable_file = "tmp"
code_file = "tmp.cpp"

def judge_compile():
    compile_error = subprocess.run(["g++", "-std=c++20", "-P", "-I", "/Users/hoangle/Other/thesis/thesis-codecontest-solver", "-o", executable_file, code_file], capture_output=True).stderr.decode('utf-8')
    if len(compile_error) > 0:
        return compile_error    
    return "Compile Success"

def judge_output(test_output, code_output):
    test_output = test_output.strip().split()
    code_output = code_output.strip().split()
    if len(test_output) != len(code_output):
        return False
    for i in range(len(test_output)):
        try:
            test = int(test_output[i])
            code = int(code_output[i])
            if test != code:
                return False
        except ValueError:
            try:
                test = float(test_output[i])
                code = float(code_output[i])
                if abs(test - code) > 1e-6:
                    return False
            except ValueError:
                if test_output[i] != code_output[i]:
                    return False
    return True

def judge_tests(tests):
    for test in tests:
        test_input, test_output = test
        try:
            completed_process = subprocess.run(['timeout', '2s', f'./{executable_file}'], input=test_input, capture_output=True, text=True, timeout=5)
            code_output = completed_process.stdout.strip()
        except subprocess.TimeoutExpired:
            return f"Time Limit Exceeded on input: {test_input}"
        except subprocess.CalledProcessError as e:
            return f"Runtime Error: {e.stderr}"
        except MemoryError:
            return f"Memory Error on input: {test_input}"
        if not judge_output(test_output, code_output):
            return f"Input: {test_input}\nExpected: {test_output}\nGot: {code_output}\n"
    return "OK"

def judge(code, tests):
    with open(code_file, 'w') as f:
        f.write(code)
    compile_result = judge_compile()
    if compile_result != "Compile Success":
        return False, compile_result
    return True, judge_tests(tests)

