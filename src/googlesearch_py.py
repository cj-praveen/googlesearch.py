from typing import Dict, List, Union
import httpx
import re

headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }

def search(query: str, max_results: int = 10, include_content: bool = False) -> List[Union[dict, str]]:
    """
    :param query: The query that you want to get results for

    :param max_results: The maximum number of results

    :param include_content: If set to True, it will scrape the site for contents

    :return: If results are available for your search query, it will
    return a list containing dict objects; otherwise, it will return an empty list.
    """

    results: List[Union[dict, str]] = []
    
    base_url: str = "https://www.google.com/search?q={}&num=30&hl=en"

    page: str = httpx.get(base_url.format(query), headers=headers).text

    pattern: str = '<div class="yuRUbf"><a href="(.*?)" data-jsarwt=".*?" ' \
                   'data-usg=".*?" data-ved=".*?"><br><h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>.*?' \
                   '<div class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf" style="-webkit-line-clamp:2">' \
                   '<span>(.*?)</span></div>'

    for i in re.findall(pattern=pattern, string=page)[:max_results if max_results else 10]:
        data: Dict[str, str] = dict(url = i[0], title = i[1], description = re.sub('<[^<>]+>', '', i[2]))

        results.append(data | dict(content = httpx.get(i[0], headers=headers).text)) if include_content else results.append(data)

    return results
