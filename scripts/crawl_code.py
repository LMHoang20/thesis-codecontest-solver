import asyncio
from download_code import get, get_parser
import sys

url = sys.argv[1]

parser = get_parser(url)
content = asyncio.run(get(url))
if content == 'failed':
    print('Failed')
    sys.exit(0)

code, language = parser.parse_content(content)
print(f'Language: {language}\nCode:\n{code}')