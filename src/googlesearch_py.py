from typing import Union, List, Dict
import httpx
import re


def search(query: str, num: int = 10, headers: Union[Dict[str, str], None] ={"User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}) -> List[Union[dict, str]]:

    results: List[Union[dict, str]] = []

    base_url: str = "https://www.google.com/search?q={}&num=30&hl=en"

    page: str = httpx.get(base_url.format(query), headers=headers).text

    web: str = '<div class="yuRUbf"><a href="(.*?)" data-jsarwt=".*?" ' \
                   'data-usg=".*?" data-ved=".*?"><br><h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>.*?' \
                   '<div class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf" style="-webkit-line-clamp:2">' \
                   '<span>(.*?)</span></div>'

    for i in re.findall(pattern=web, string=page):
        results.append({
            "url": i[0],
            "title": i[1],
            "description": re.sub('<[^<>]+>', '', i[2])
        })

    return results[:num if len(results) > num else len(results)]
