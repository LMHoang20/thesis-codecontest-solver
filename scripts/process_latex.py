import sys
import subprocess

file_name = sys.argv[1]

result = ""

code = ""

separator = ['# TUTORIAL CODE XXX', 'zxcv']

with open(file_name, 'r') as f:
    data = f.read()
    for sep in separator:
        start_code = data.find(sep)
        if start_code != -1:
            code = data[start_code + len(sep):]
            data = data[:start_code]
    data = data.replace('\\[', '$')
    data = data.replace('\\]', '$')
    if 'latex:' in data:
        while True:
            dollar_1 = data.find('$')
            dollar_2 = data.find('$', dollar_1 + 1)
            dollar_3 = data.find('$', dollar_2 + 1)
            dollar_4 = data.find('$', dollar_3 + 1)
            if dollar_3 != -1 and dollar_4 != -1:
                if "latex:" in data[dollar_2:dollar_3]:
                    latex_fomula = data[dollar_3:dollar_4 + 1]
                    actual_latex_fomula = latex_fomula[1:-1]
                    actual_latex_fomula = actual_latex_fomula.strip()
                    result += data[:dollar_1] + f'${actual_latex_fomula}$'
                    data = data[dollar_4 + 2:]
                else:
                    result += data[:dollar_1 + 1]
                    data = data[dollar_1 + 2:]
            else:
                result += data
                break
    else:
        result = data

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

            subprocess.run(["python", "scripts/normalize_code.py", "tmp.cpp"])

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