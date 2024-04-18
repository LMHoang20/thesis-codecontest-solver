import scrapy
import json
import time
import asyncio
import sys

from playwright.async_api import async_playwright
from constants import *


async def crawl(url, contest_id, output_file):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url)
            time.sleep(2)
            for attempt in range(15):
                print("Attempt number", attempt)
                html = await page.content()
                content = scrapy.Selector(
                    text=html).xpath('//div[@class="content"]').get()
                if "Tutorial is loading..." in content:
                    print("Tutorial is loading...")
                    continue
                if "MJXp" in content:
                    print("Mathjax is loading...")
                    continue
                if "$$$" in content:
                    print("$$$ is loading...")
                    continue
                break
            else:
                return 'failed'
        except Exception:
            return 'failed'
        output_file.write(content)
        await context.clear_cookies()
        await browser.close()
        return output_file


def main():
    contest_id = sys.argv[1]
    url = sys.argv[2]
    output_file = open('meow.html', 'w')
    result = asyncio.run(crawl(url, contest_id, output_file))
    print(result)
    if result == 'failed':
        return
    os.system('python html2text/html_analyze_single.py')
    with open('meow.md', 'r') as infile:
        content = infile.read()
    

if __name__ == "__main__":
    main()
