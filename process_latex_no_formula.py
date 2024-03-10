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

if '```cpp' in code:
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
            f.write("\n# TUTORIAL CODE XXX\n\n```cpp")
            f.write(code)
            f.write("```\n")
else:
    with open(file_name, 'w') as f:
        f.write(result)
        if code != "":
            f.write("\n# TUTORIAL CODE XXX\n\n")
            f.write(code)
            f.write("\n")
