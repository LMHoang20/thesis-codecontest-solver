import os

# delete python package cache folders
for root, dirs, files in os.walk('.'):
    for dir in dirs:
        if dir == '__pycache__':
            _dir = os.path.join(root, dir)
            print(_dir)
            os.system(f'rm -rf {_dir}')

