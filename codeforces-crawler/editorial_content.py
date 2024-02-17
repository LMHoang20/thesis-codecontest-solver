import scrapy
import json
import time
import asyncio

from playwright.async_api import async_playwright
from constants import *

async def crawl(starting_points, success_file, fail_file, offset=0, retry=0):
    async with async_playwright() as pw:              
        browser = await pw.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        for i, data in enumerate(starting_points[offset:]):
            url = data['editorial_url']
            problem_url = data['url']
            
            print("Crawling start", url)
            try:
                await page.goto(url)
                time.sleep(2)
                success = True
                for attempt in range(15):
                    print("Attempt number", attempt)
                    html = await page.content()
                    content = scrapy.Selector(text=html).xpath('//div[@class="content"]').get()
                    if "Tutorial is loading..." in content:
                        continue
                    if "MJXp" in content:
                        continue
                    if "$$$" in content:
                        continue
                    break
                else:
                    success = False
            except Exception:
                return {
                    "retry": retry + 1,
                    "offset": offset + i,
                }

            if not success:
                json.dump(data, fail_file)
                fail_file.write('\n')
            else:
                json.dump({
                    "url": url,
                    "problem_url": problem_url,
                    "content": content
                }, success_file)
                success_file.write('\n')
        
            await context.clear_cookies()
            print("Crawling done", url)
        await browser.close()

def main():
    starting_points = []
    with open(CLEAN_EDITORIAL_URLS_PATH, "r") as file:
        for line in file:
            data = json.loads(line)
            starting_points.append(data)

    with open(EDITORIAL_CONTENT_PATH, 'w') as success_file:
        with open(EDITORIAL_CONTENT_FAIL_PATH, 'w') as fail_file:
            result = asyncio.run(crawl(starting_points, success_file, fail_file))
            while result != None:
                time.sleep(10)
                if result['retry'] > 3:
                    fail_file.write(json.dumps(starting_points[result['offset']]))
                    fail_file.write('\n')
                    result = asyncio.run(crawl(starting_points, success_file, fail_file, result['offset'] + 1))
                else:
                    result = asyncio.run(crawl(starting_points, success_file, fail_file, result['offset'], result['retry']))

if __name__ == "__main__":
    main()