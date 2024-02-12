import scrapy
import os
from dotenv import load_dotenv

class EditorialURLSpider(scrapy.Spider):
    name = "editorial_url"
    allowed_domains = ["codeforces.com"]
    start_urls = []

    load_dotenv()
    PROBLEM_URLS_PATH = os.getenv("PROBLEM_URLS_PATH")

    with open(PROBLEM_URLS_PATH, "r") as file:
        for line in file:
            start_urls.append(line.strip())

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        editorial_selectors = response.selector.xpath(
            "//div[@class='roundbox sidebox sidebar-menu borderTopRound ']/ul/li/span/a"
        )

        results = []
        for selector in editorial_selectors:
            url = selector.xpath("@href").get()
            if url == None:
                url = ""
            if url.startswith("/"):
                url = response.urljoin(url)
            title = selector.xpath("string()").get()
            results.append({"title": title, "url": url})
            
        yield {
            "result": results,
            "url": response.url,
        }
            
    