import re

mklinks = re.compile(r'\[(.+)\]\((.+)\)')

txt = "The rain in [xyz](abc) Spain"
x = re.findall(mklinks, txt)
print(x)