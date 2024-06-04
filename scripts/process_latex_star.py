import os 
import sys 

def isWhiteSpace(c):
    return c == ' ' or c == '\n' or c == '\t'

def main():
    file_name = sys.argv[1]
    tutorial = ""
    with open(file_name, 'r') as f:
        content = f.read()
        name = content[content.find('<NAME>') + len('<NAME>'):content.find('</NAME>')].strip()
        tutorial = content[content.find('<TUTORIAL>') + len('<TUTORIAL>'):content.find('</TUTORIAL>')].strip()

        if name not in tutorial:
            return 'wtf'
        
        star_count = tutorial.count('*') - 2 * tutorial.count('**')
        if star_count % 2 == 1:
            return 'odd number of stars'
        result = ""
        while '*' in tutorial:
            first_star = tutorial.find('*')
            if tutorial[first_star + 1] == '*':
                result += tutorial[:first_star + 2]
                tutorial = tutorial[first_star + 2:]
                continue
            last_star = tutorial.find('*', first_star + 1)
            for i in range(last_star + 1, len(tutorial)):
                if tutorial[i] == '*':
                    last_star = i
                elif isWhiteSpace(tutorial[i]):
                    break
            formula = tutorial[first_star:last_star + 1]
            formula = formula.replace('*', '')
            result += tutorial[:first_star] + f'${formula}$'
            tutorial = tutorial[last_star + 1:]
        result += tutorial
    with open(file_name, 'w') as f:
        f.write('<ANSWER>\n')
        f.write('<NAME>\n')
        f.write(name)
        f.write('\n')
        f.write('</NAME>\n')
        f.write('<TUTORIAL>\n')
        f.write(result)
        f.write('\n')
        f.write('</TUTORIAL>\n')
        f.write('</ANSWER>\n')
    return 'done'
        
if __name__ == '__main__':
    print(main())