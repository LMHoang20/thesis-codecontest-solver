with open('notes/sus.txt', 'r') as f:
    lines = f.readlines()

scripts = []

script = '!pip install --force-reinstall --use-pep517 -q'

for line in lines:
    line = line.split()
    package = line[0]
    version = line[1]
    if '+' in version:
        continue
    script += f' {package}=={version}'
    
print(script)