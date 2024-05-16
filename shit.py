import re
import os
from bs4 import BeautifulSoup


def get_all_text(tag):
    if tag.string:
        return tag.string.strip()
    ans = ""
    space = False
    for child in tag.children:
        if space:
            ans += " "
        ans += get_all_text(child)
        space = True
    return ans

for i in range(1, 3114):
    error_list = []
    if not os.path.exists(str(i) + '.html'):
        continue
    with open(str(i) + '.html', 'r') as file:
        with open('md/' + str(i) + '.md', 'w') as md_file:
            try:
                soup = BeautifulSoup(file.read(), 'html.parser')
                title = soup.find('title').string.strip()
                md_file.write(f'# {title}\n\n')
                md_file.write('## Description:\n')

                description_header = soup.find('h2', id='description')
                solution_header = soup.find('h2', id='solutions')

                constraints_strong_tag = soup.find('strong', string=re.compile(r'\s*Constraints:\s*'))
                constraints_header = constraints_strong_tag.find_parent('p')

                p_tags = soup.find_all('p')
                description_parts = []
                for p_tag in p_tags:
                    if p_tag == description_header.find_next('p'):
                        while p_tag.find_next_sibling() != constraints_header:
                            text = get_all_text(p_tag).strip()
                            text = ' '.join(text.split())
                            text = text.replace(' .', '.')
                            text = text.replace(' ,', ',')
                            text = text.replace(' ?', '?')
                            text = text.replace(' !', '!')
                            description_parts.append(text)

                            if "Example " in text:
                                pre_tag = p_tag.find_next('pre')
                                description_parts.append(get_all_text(pre_tag).strip())
                            p_tag = p_tag.find_next_sibling('p')
                description = '\n'.join(description_parts)
                md_file.write(description)

                # Find the next 'ul' tag
                constraints_list = constraints_header.find_next('ul')

                # # Extract the text from the 'Constraints:' header and the 'ul' tag
                constraints_text = constraints_header.get_text(strip=True) + '\n'
                for li in constraints_list.find_all('li'):
                    for sup in li.find_all('sup'):
                        sup.replace_with('^' + sup.get_text(strip=True))
                    constraints_text += li.get_text(strip=True) + '\n'

                # # Print the constraints
                md_file.write(constraints_text)
                md_file.write('\n')

                p_tags = soup.find_all('p')
                solution_parts = []
                for p_tag in p_tags:
                    if p_tag == solution_header.find_next('p'):
                        while p_tag is not None:
                            text = get_all_text(p_tag).strip()
                            text = ' '.join(text.split())
                            text = text.replace(' .', '.')
                            text = text.replace(' ,', ',')
                            text = text.replace(' ?', '?')
                            text = text.replace(' !', '!')
                            if "Solution" in text:
                                text = "## " + text
                            solution_parts.append(text)
                            p_tag = p_tag.find_next_sibling('p')
                solution = '\n'.join(solution_parts)
                md_file.write(solution)
                md_file.write("## Code:")
                soup.find('h2', id='description')
                code = soup.find('div', {'class': 'language-cpp highlighter-rouge'})
                if code is None:
                    code = soup.find('div', {'class': 'language-py highlighter-rouge'})
                md_file.write("```")
                md_file.write(code.get_text().strip())
                md_file.write("```")
            except Exception as e:
                # delete the file i.md if an error occurs
                os.remove("md/" + str(i) + '.md')
                error_list.append(i)