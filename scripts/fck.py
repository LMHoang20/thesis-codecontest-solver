import os


roots = []
for root, dirs, files in os.walk('data/contests-v2', topdown=False):
    for file in files:
        if file == 'editorial.md':
            with open(os.path.join(root, file), 'r') as f:
                content = f.read()
                if 'assert' in content:
                    roots.append(root)
                if 'LASSERT' in content:
                    print(root)

print()
roots = sorted(list(set(roots)), key=lambda x: int(x.split('/')[-1]))
for root in roots:
    print(root + '/editorial.md')