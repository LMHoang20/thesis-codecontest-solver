with open("/Users/hoangle/Other/thesis/thesis-codecontest-solver/notes/prompt.tex", "r") as f:
    content = f.read()

content = content.split('\n')

for i in range(8):
    for j in range(10):
        print('& ' + content[i+j*8], end=' ')
    print()