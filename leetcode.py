import os


for root, dirs, files in os.walk('./data/md'):
    for file in files:
        if file.endswith('.py'):
            print(file)