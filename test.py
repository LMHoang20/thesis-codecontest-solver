import os 

for root, dirs, files in os.walk('data/contests'):
    for file in files:
        if file != 'editorial.md' and '-' not in file and file.endswith('.md'):
            dir = os.path.join(root, file)
            print(dir)
            with open(dir, 'r') as f:
                first_line = f.readlines()[0]
            with open('test.txt', 'a') as f:
                f.write(f"{dir}:\n{first_line}\n\n")

for root, dirs, files in os.walk('data/contests-v2'):
    for file in files:
        if file != 'editorial.md' and '-' not in file and file.endswith('.md'):
            dir = os.path.join(root, file)
            print(dir)
            with open(dir, 'r') as f:
                first_line = f.readlines()[0]
            with open('test.txt', 'a') as f:
                f.write(f"{dir}:\n{first_line}\n\n")
                