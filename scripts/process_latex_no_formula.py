import sys
import subprocess

file_name = sys.argv[1]

result = ""

code = ""

separator = ['# TUTORIAL CODE XXX', 'zxcv']

with open(file_name, 'r') as f:
    data = f.read()
    start_code = data.find("# TUTORIAL CODE XXX")
    if start_code != -1:
        code = data[start_code + len("# TUTORIAL CODE XXX"):]
        data = data[:start_code]
    while True:
        dollar_1 = data.find('$')
        dollar_2 = data.find('$', dollar_1 + 1)
        if dollar_1 != -1 and dollar_2 != -1:
            # first parenthesis to the left of dollar_1
            left_parenthesis = data.rfind('(', 0, dollar_1)
            # first parenthesis to the right of dollar_2
            right_parenthesis = data.find(')', dollar_2)
            if left_parenthesis != -1 and right_parenthesis != -1 and "latex:" in data[
                    left_parenthesis:right_parenthesis]:
                latex_fomula = data[dollar_1:dollar_2 + 1]
                result += data[:left_parenthesis - 1] + latex_fomula
                data = data[right_parenthesis + 1:]
            else:
                print("WTF")
        else:
            result += data
            break

code = code.strip()
codes = []
for sep in separator:
    if sep in code:
        codes = code.split(sep)
        break

if codes == [] and code != "":
    codes = [code]

processed_codes = []

for code in codes:
    if '```cpp' in code:
        code = code.strip()
        if code.startswith("```cpp"):
            code = code[len("```cpp"):]
        if code.endswith("```"):
            code = code[:-len("```")]

        if code != "":
            with open("tmp.cpp", 'w') as f:
                f.write(code)

            subprocess.run(["python", "normalize_code.py", "tmp.cpp"])

            with open("tmp.cpp", 'r') as f:
                code = f.read()
    
        processed_codes.append(f"\n```cpp{code}```") 
    else:
        processed_codes.append(code)

with open(file_name, 'w') as f:
    f.write(result)
    for code in processed_codes:
        f.write('\n# TUTORIAL CODE XXX\n')
        f.write(code)

with open(file_name, 'r') as f:
    data = f.read()
    data = data.strip()
    while "\n\n\n" in data:
        data = data.replace("\n\n\n", "\n\n")

with open(file_name, 'w') as f:
    f.write(data)