import typing
import httpx
import re


def search(query: str) -> typing.List[typing.Union[dict, str]]:
    """
    The Google search scraper for the Python programming language.

    :param query: The query that you want to get results for

    :return: If results are available for your search query, it will
    return a list containing dict objects; otherwise, it will return an empty list.
    """

    results: typing.List[typing.Union[dict, str]] = []

    headers: typing.Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }

    base_url: str = "https://www.google.com/search?q={}&num=30&hl=en"

    page: str = httpx.get(base_url.format(query), headers=headers).text

    pattern: str = '<div class="yuRUbf"><a href="(.*?)" data-jsarwt=".*?" ' \
                   'data-usg=".*?" data-ved=".*?"><br><h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>.*?' \
                   '<div class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf" style="-webkit-line-clamp:2">' \
                   '<span>(.*?)</span></div>'

    for i in re.findall(pattern=pattern, string=page):
        results.append({
            "url": i[0],
            "title": i[1],
            "description": re.sub('<[^<>]+>', '', i[2])
        })

    return results
