import scrapy
import json
import time
import asyncio

from playwright.async_api import async_playwright
from const_getter import ConstGetter

CLEAN_EDITORIAL_URLS_PATH = ConstGetter.get_clean_editorial_urls_path()
EDITORIAL_CONTENT_PATH = ConstGetter.get_editorial_content_path()
EDITORIAL_CONTENT_FAIL_PATH = ConstGetter.get_editorial_content_fail_path()

async def crawl(starting_points, success_file, fail_file, offset=0):
    async with async_playwright() as pw:              
        browser = await pw.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        for data, i in enumerate(starting_points[offset:]):
            url = data['editorial_url']
            problem_url = data['url']
            
            print("Crawling start", url)
            try:
                await page.goto(url)
                attempt = 1
                success = True
                while True:
                    html = await page.content()
                    content = scrapy.Selector(text=html).xpath('//div[@class="content"]').get()
                    if "Tutorial is loading..." not in content:
                        break
                    else:
                        print("Attempt fail number", attempt)
                        attempt += 1
                        if attempt == 10:
                            success = False
                            break
                        time.sleep(1)
            except Exception:
                return {
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
                result = asyncio.run(crawl(starting_points, success_file, fail_file, result['offset']))

if __name__ == "__main__":
    main()