import bs4
import json
import os

from constants import *
from lxml import etree


def mathml2latex_yarosh(equation):
    xslt_file = os.path.join("mathconverter", "xsl_yarosh", "mmltex.xsl")
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return str(newdom)


def extract_element_text(element):
    if isinstance(element, bs4.NavigableString):
        return element.string
    for child in element.children:
        if isinstance(child, bs4.NavigableString):
            return child.string
        if isinstance(child, bs4.Tag):
            return extract_element_text(child)
    raise Exception(f'Unknown type: {type(element)}, {element}')


def handle_span(element):
    if "data-mathml" in element.attrs:
        return mathml2latex_yarosh(element["data-mathml"])
    if "class" not in element.attrs:
        return parse(element)
    if "id" in element.attrs and "MathJax" in element["id"]:
        return ""
    result = parse(element)
    for class_name in element["class"]:
        if "MJXp" in class_name:
            return ""
        match class_name:
            case "tex-font-style-tt":
                result = f"`{result}`"
            case "tex-font-style-it":
                result = f"*{result}*"
            case "tex-font-style-bf":
                result = f"**{result}**"
            case "tex-font-style-underline":
                result = f"_{result}_"
            case "tex-font-style-striked":
                result = f"~~{result}~~"
            case "tex-font-style-section":
                result = f"\n\n## {result}"
            case "tex-font-style-subsection":
                result = f"\n\n### {result}"
            case "tex-font-size-small":
                result = f"{result}"
            case "tex-font-size-large":
                result = f"{result}"
            case "tex-span":
                result = f"${result}$"
            case "legendary-user-first-letter":
                result = result
            case "MathJax_Preview":
                result = result
            case "MathJax_Processing":
                result = result
            case "MathJax":
                result = result
            case "apple-style-span":
                result = result
            case "Apple-style-span":
                result = result
            case "undefined":
                result = result
            case "":
                result = result
            case _:
                raise Exception(
                    f'Unknown span class: {element["class"]}, {element.prettify()}'
                )
    return result


def handle_div(element):
    if "class" not in element.attrs:
        return f"{parse(element)}\n"
    if len(element["class"]) == 1:
        class_name = element["class"][0]
        match class_name:
            case "ttypography":
                return f"{parse(element)}\n"
            case "problem-statement":
                return f"{parse(element)}\n"
            case "spoiler":
                return f"{parse(element)}\n"
            case "spoiler-title":
                return f"# {parse(element)}\n"
            case "spoiler-content":
                return f"{parse(element)}\n"
            case "MathJax_Display":
                return f"{parse(element)}\n"
            case "header":
                return f"{parse(element)}\n"
            case "title":
                return f"\n# {parse(element)}\n"
            case "from-renderer":
                return f"{parse(element)}\n"
            case "epigraph":
                return ""
            case _:
                raise Exception(
                    f'Unknown div class: {element["class"]}, {element.prettify()}'
                )
    raise Exception(
        f'Multiple div class: {element["class"]}, {element.prettify()}')


def handle_tag(tag, element):
    match tag:
        case 'strong':
            return f'**{parse(element)}** '
        case 'b':
            return f'**{parse(element)}** '
        case 'em':
            return f'*{parse(element)}* '
        case "u":
            return f"_{parse(element)}_ "
        case 'h1':
            return f'\n# {parse(element)}\n\n'
        case 'h2':
            return f'\n## {parse(element)}\n\n'
        case 'h3':
            return f'\n### {parse(element)}\n\n'
        case 'h4':
            return f'\n#### {parse(element)}\n\n'
        case 'h5':
            return f'\n##### {parse(element)}\n\n'
        case 'h6':
            return f'\n###### {parse(element)}\n\n'
        case 'p':
            return f'{parse(element)}\n\n'
        case 'a':
            if "href" not in element.attrs:
                return parse(element)
            return f'[{parse(element)}]({element["href"]})'
        case 'div':
            return handle_div(element)
        case 'span':
            return handle_span(element)
        case 'i':
            return f'{parse(element)}'
        case "script":
            return f" (latex: ${parse(element)}$)"
        case 'ul':
            return parse(element)
        case 'ol':
            return parse(element)
        case 'li':
            return f"- {parse(element)}\n"
        case 'sub':
            element = parse(element)
            if len(element) == 1:
                return f"_{element}"
            return "_{" + element + "}"
        case 'sup':
            element = parse(element)
            if len(element) == 1:
                return f"^{element}"
            return "^{" + element + "}"
        case 'code':
            return f"`{parse(element)}`"
        case 'pre':
            return f"\n```\n{element.get_text()}\n```\n"
        case 'hr':
            return "---\n"
        case 'br':
            return "\n"
        case 'nobr':
            return parse(element)
        case 'center':
            return parse(element)
        case 'table':
            return ""
        case 'font':
            return parse(element)
        case 'strike':
            return f"~~{parse(element)}~~"
        case 's':
            return f"~~{parse(element)}~~"
        case 'blockquote':
            return f"> {parse(element)}"
        case 'dl':
            return parse(element)
        case 'dd':
            return f"{parse(element)}"
        case 'img':
            alt = element.get('alt', '')
            src = element.get('src', '')
            return f"![{alt}]({src})"
        case _:
            raise Exception(f'Unknown tag: {tag}, {element.prettify()}')


def parse(element):
    result = ""
    for child in element.children:
        if isinstance(child, bs4.NavigableString):
            result += child.string
        elif isinstance(child, bs4.Tag):
            result += handle_tag(child.name, child)
        else:
            raise Exception(f'Unknown type: {type(child)}, {child}')
    return result

if __name__ == "__main__":
    done_urls = set()

    BLACK_LIST = [
        "https://codeforces.com/blog/entry/906",
    ]

    print(CLEAN_EDITORIAL_CONTENT_PATH)
    print(EDITORIAL_TO_REVIEW_PATH)
    print(EDITORIAL_CONTENT_PATH)

    with open(CLEAN_EDITORIAL_CONTENT_PATH, 'w') as outfile:
        with open(EDITORIAL_TO_REVIEW_PATH, 'w') as review:
            with open(EDITORIAL_CONTENT_PATH, 'r') as file:
                for line in file:
                    data = json.loads(line)
                    if data['url'] in done_urls:
                        continue
                    if data['url'] in BLACK_LIST:
                        continue
                    done_urls.add(data['url'])
                    content = data['content']
                    try:
                        soup = bs4.BeautifulSoup(content, 'html.parser')
                    except Exception as e:
                        print("error", e)
                        print("url", data['url'])
                        review.write(data['url'])
                        review.write('\n')
                        continue
                    element = soup.select('div.content')[0].select(
                        'div.ttypography')[0]
                    try:
                        content = parse(element)
                        content = content.replace("$$$", "$")
                        content = content.replace("veryverythinmathspace",
                                                "0.05555555555555555em")
                        content = content.replace("verythinmathspace",
                                                "0.1111111111111111em")
                        content = content.replace("thinmathspace",
                                                "0.16666666666666666em")
                        content = content.replace("mediummathspace",
                                                "0.2222222222222222em")
                        content = content.replace("thickmathspace",
                                                "0.2777777777777778em")
                        content = content.replace("verythickmathspace",
                                                "0.3333333333333333em")
                        content = content.replace("veryverythickmathspace",
                                                "0.3888888888888889em")
                        out = {"url": data['url'], "content": content}
                        json.dump(out, outfile)
                        outfile.write('\n')
                    except Exception as e:
                        print("error", e)
                        print("url", data['url'])
                        if "Image tag" in str(e):
                            review.write(json.dumps(data['url']))
                            review.write('\n')
                            continue
                        else:
                            raise e
