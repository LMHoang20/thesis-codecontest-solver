import scrapy
import json

from const_getter import ConstGetter

def parse(selector):
    result = ""
    for element in selector.xpath('./*'):
        match element.tag:
            case 'p':
                result += f'{parse(element)}\n'
            case 'ul':
                result += f'{parse(element)}\n'
            case 'ol':
                result += f'{parse(element)}\n'
            case 'li':
                result += f'\t•\t{parse(element)}\n'
            case 'div':
                result += f'{parse(element)}\n'
            case 'span':
                result += f'{parse(element)}'
            case 'pre':
                result += f'{parse(element)}\n'
            case 'a':
                result += f'Link: {element.xpath("@href").get()}\nContent: {parse(element)}\n'
            case 'br':
                result += '\n'
            case 'text':
                result += element.get()
            case 'h1':
                result += f'# {parse(element)}\n'
            case 'h2':
                result += f'## {parse(element)}\n'
            case 'h3':
                result += f'### {parse(element)}\n'
            case 'h4':
                result += f'#### {parse(element)}\n'
            case 'h5':
                result += f'##### {parse(element)}\n'
            case 'h6':
                result += f'###### {parse(element)}\n'
            case _:
                print(f'Unknown tag: {element.tag}')
    return result

EDITORIAL_CONTENT_PATH = ConstGetter.get_editorial_content_path()

with open(EDITORIAL_CONTENT_PATH, 'r') as file:
    for line in file:
        data = json.loads(line)
        content = data['content']
        selector = scrapy.Selector(text=content)
        selector = selector.xpath('//div[@class="content"]/div[@class="ttypography"]')



