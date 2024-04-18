import bs4
from html_analyze import parse

with open('meow.html') as infile:
    content = infile.read()

soup = bs4.BeautifulSoup(content, 'html.parser')
element = soup.select('div.content')[0].select('div.ttypography')[0]
content = parse(element)
content = content.replace("$$$", "$")

with open('meow.md', 'w') as outfile:
    outfile.write(content)