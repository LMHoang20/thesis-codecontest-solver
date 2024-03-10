import sys
import subprocess

file_name = sys.argv[1]

result = ""

with open(file_name, 'r') as f:
    result = f.read()

last_include = result.rfind("#include")
last_include += result[last_include:].find("\n")

includes = result[:last_include]

result = includes + "\nint end_includes;\n" + result[last_include:]

with open(file_name, 'w') as f:
    f.write(result)

preprocessed = subprocess.run(["gcc", "-E", file_name],
                              capture_output=True,
                              text=True).stdout

end_includes = preprocessed.find("int end_includes;")

preprocessed = includes + "\n" + preprocessed[end_includes +
                                              len("int end_includes;"):]

preprocessed = preprocessed.split("\n")

with open(file_name, 'w') as f:
    f.write(includes + "\n")
    for line in preprocessed:
        if line == "":
            continue
        if line[0] == '#':
            continue
        if line.find('tmp.cpp') != -1:
            continue
        if line.find('"<built-in>"') != -1:
            continue
        result = line
        f.write(result + '\n')

formatted = subprocess.run(["clang-format", file_name], capture_output=True, text=True).stdout

with open(file_name, 'w') as f:
    f.write(formatted)