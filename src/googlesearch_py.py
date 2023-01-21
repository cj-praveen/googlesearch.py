import typing
import httpx
import re

headers: typing.Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }

def search(query: str, max_results:int=0, get_contents:bool=False, process_function:typing.Callable=lambda text,*a,**kw : text, *args, **kwargs) -> typing.List[typing.Union[dict, str]]:
    """
    The Google search scraper for the Python programming language.

    :param query: The query that you want to get results for

    :param max_results: The maximum number of results

    :param get_contents: If set to True, it will scrape the site for contents

    :param process_function: (optional) function to process the site's contents before returning the results


    :return: If results are available for your search query, it will
    return a list containing dict objects; otherwise, it will return an empty list.
    """

    results: typing.List[typing.Union[dict, str]] = []
    
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

    if max_results != 0:
        results = results[:abs(max_results)]
    
    if get_contents:
        for result in results:
            result["contents"] = scrape(result["url"], process_function=process_function, get_metadata=False)["contents"]

    return results

def scrape(url, process_function=lambda text,*a,**kw : text, get_metadata = True, *args, **kwargs) -> typing.Dict[str, str]:
    if isinstance(url,list):
        print(f"Scraping multiple urls... {url}")
        multiResults ={}
        for u in url:
            multiResults[url] = scrape(u, process_function=process_function, *args, **kwargs)
        return multiResults

    final_results: typing.Dict[str, str] = {
        "contents": httpx.get(url, headers=headers).text,
        "url":url
         }
    final_results["contents"] = process_function(final_results["contents"], *args, **kwargs)
    # Get the title and description of the url by using search
    if get_metadata:
        searched = search(query=url, max_results = 1, get_contents=False)
        if len(searched) > 0:
            for k in searched[0]:
                final_results[k] = searched[0][k]
        
    return final_results
