import requests 
import bs4
import re
import os
import psycopg2
import threading
import time
import asyncio
from playwright.async_api import async_playwright

class Logger():
    def __init__(self, file_name):
        self.file_name = file_name
        self.mutex = threading.Lock()
    def log(self, message):
        with self.mutex:
            with open(self.file_name, 'a') as f:
                f.write(f'{message}\n')
            print(message)

logger = Logger('log.txt')

def get_db_conn():
    return psycopg2.connect(database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432'
)

def create_table():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        url TEXT PRIMARY KEY,
        contest_id TEXT,
        problem_id TEXT,
        placeholder TEXT,
        code TEXT,
        language TEXT
    );
    ''')
    conn.commit()
    cursor.close()

def insert_link(filedir, placeholder, url, code, language):
    conn = get_db_conn()
    cursor = conn.cursor()
    def escape(s):
        return s.replace("'", "''")
    def contest_id():
        return filedir.split('/')[2]
    def problem_id():
        problem_id = filedir.split('/')[-1]
        if problem_id.endswith('.md'):
            problem_id = problem_id[:-3]
        return problem_id
    cursor.execute('''
    INSERT INTO links (contest_id, problem_id, placeholder, url, code, language) VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING
    ''', (contest_id(), problem_id(), escape(placeholder), url, escape(code), language))
    conn.commit()
    cursor.close()

API = 'http://archive.org/wayback/available'

def get_archive_url(url):
    params = {'url': url}
    response = requests.get(API, params=params)
    data = response.json()
    try:
        return data['archived_snapshots']['closest']['url']
    except:
        return None

async def get(url):
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        url = 'https://codeforces.com' + url
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            if 'pastebin.com' in url:
                await page.wait_for_selector('ol')
            elif 'ideone.com' in url:
                await page.wait_for_selector('pre')
            else:
                await page.wait_for_selector('table')
            content = await page.content()
            await browser.close()
            return content
    except:
        if 'archive' in url:
            return 'failed'
        archived_url = get_archive_url(url)
        if archived_url is None:
            return 'failed'
        return await get(archived_url)

class Pastebin():
    def parse_content(self, content):
        content = bs4.BeautifulSoup(content, 'html.parser')
        content = content.find_all('ol')[0]
        language = content.get('class')[0]
        return content.text, language

class Ideone():    
    def parse_content(self, content):
        content = bs4.BeautifulSoup(content, 'html.parser')
        content = content.find_all('pre')[1]
        language = content.get('class')[0]
        result = ''
        for line in content.find_all('li'):
            result += line.text + '\n'
        return result, language

class Codeforces():
    def parse_content(self, content):
        content = bs4.BeautifulSoup(content, 'html.parser')
        table = content.find_all('table')[0]
        language = table.find_all('td')[3].text
        content = content.find_all('pre', id='program-source-text')[0]
        result = ''
        for line in content.find_all('li'):
            result += line.text + '\n'
        return result, language.strip()

def get_parser(url):
    if 'ideone.com' in url:
        return Ideone()
    elif 'pastebin.com' in url:
        return Pastebin()
    return Codeforces()

mdLinks = re.compile(r'\[(.+)\]\(((?:(?:/|//codeforces.com/)contest/\d+/submission/|http).+)\)')

urls = [
    ('', 'https://pastebin.com/qMfEbpyi'),
    ('', 'https://ideone.com/w8ch4w'),
    ('', 'https://codeforces.com/contest/456/submission/7407631')
]

def notCrawl(url):
    return 'submission' not in url and 'pastebin' not in url and 'ideone' not in url

async def crawl(filedir, placeholder, url):
    try:
        content = await get(url)
        if content == 'failed':
            return 'failed'
        parser = get_parser(url)
        code, language = parser.parse_content(content)
        insert_link(filedir, placeholder, url, code, language)
        return 'done'
    except Exception as e:
        return f'failed {e}'

cntUrl = dict()

DEFAULT_WAIT_TIME = 3
MAX_WAIT_TIME = 60
DEFAULT_RETRY = 10

async def worker(links):
    waitTime = DEFAULT_WAIT_TIME
    while len(links) > 0:
        link = links[0]
        links = links[1:]
        logger.log(f'{link}: start')
        status = await crawl(*link)
        logger.log(f'{link}: {status}')
        if status.startswith('failed'):
            cntUrl[link[2]] = cntUrl.get(link[2], 0) + 1
            if cntUrl[link[2]] > DEFAULT_RETRY:
                logger.log(f'{link}: failed more than {DEFAULT_RETRY} times, skip')
                continue
            links.append(link)
            time.sleep(waitTime)
            waitTime = min(MAX_WAIT_TIME, waitTime*2)
        else:
            waitTime = DEFAULT_WAIT_TIME

def check_already_downloaded(url):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM links WHERE url = %s', (url,))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

if __name__ == '__main__':
    placeholders = []
    urls = []
    filedirs = []
    for root, dirs, files in os.walk('data/contests-v2'):
        for dir in dirs:
            for _, _, files in os.walk(os.path.join(root, dir)):
                for file in files:
                    if file == 'editorial.md':
                        continue
                    filedir = os.path.join(root, dir, file)
                    with open(filedir, 'r') as f:
                        lines = f.readlines()
                        lines = lines[1:]
                        for line in lines:
                            for match in re.findall(mdLinks, line):                                
                                placeholder, url = match
                                if '[' in placeholder:
                                    placeholder = placeholder[placeholder.rfind('[')+1:]
                                if ')' in url:
                                    url = url[:url.find(')')]
                                if not notCrawl(url):
                                    placeholders.append(placeholder)
                                    urls.append((url))
                                    filedirs.append(filedir)
                                    link = f'[{placeholder}]({url})'
                                    assert link == line.strip()
    links = [(filedir, placeholder, url) for filedir, placeholder, url in zip(filedirs, placeholders, urls)]
    links = [link for link in filter(lambda link: not check_already_downloaded(link[2]), links)]
    # exit(0)
    create_table()
    ideoneLinks = [link for link in links if 'ideone' in link[2]]
    pastebinLinks = [link for link in links if 'pastebin' in link[2]]
    codeforcesLinks = [link for link in links if link not in ideoneLinks and link not in pastebinLinks]
    assert len(links) == len(ideoneLinks) + len(pastebinLinks) + len(codeforcesLinks)
    # testing
    # ideoneLinks = ideoneLinks[:1]
    # pastebinLinks = pastebinLinks[:1]
    # codeforcesLinks = codeforcesLinks[:1]
    # run all 3 types of links in parallel
    threads = []
    threads.append(threading.Thread(target=lambda: asyncio.run(worker(ideoneLinks))))
    threads.append(threading.Thread(target=lambda: asyncio.run(worker(pastebinLinks))))
    threads.append(threading.Thread(target=lambda: asyncio.run(worker(codeforcesLinks))))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
                   
    

    
