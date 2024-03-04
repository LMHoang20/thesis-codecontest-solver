import sys
import subprocess

file_name = sys.argv[1]

result = ""

code = ""

with open(file_name, 'r') as f:
    data = f.read()
    start_code = data.find("# TUTORIAL CODE XXX")
    if start_code != -1:
        code = data[start_code + len("# TUTORIAL CODE XXX"):]
        data = data[:start_code]
    while True:
        dollar_1 = data.find('$')
        dollar_2 = data.find('$', dollar_1 + 1)
        dollar_3 = data.find('$', dollar_2 + 1)
        dollar_4 = data.find('$', dollar_3 + 1)
        if dollar_3 != -1 and dollar_4 != -1:
            if "latex:" in data[dollar_2:dollar_3]:
                latex_fomula = data[dollar_3:dollar_4 + 1]
                result += data[:dollar_1] + latex_fomula
                data = data[dollar_4 + 2:]
            else:
                result += data[:dollar_1 + 1]
                data = data[dollar_1 + 2:]
        else:
            result += data
            break


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

with open(file_name, 'w') as f:
    f.write(result)
    if code != "":
        f.write("\n\n# TUTORIAL CODE XXX\n\n```cpp")
        f.write(code)
        f.write("```\n")