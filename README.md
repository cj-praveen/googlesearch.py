# googlesearch.py
The Google search scraper for the Python programming language.

## Installation instruction
- Python 3.6 or later is required.
- make sure the latest pip version is installed in your working environment.

**If you meet the above requirements, run the following command given below to install the latest version of googlesearch.py:**
```
pip install -U googlesearch.py
```

## Get Started
Here is an example program.
```py
import googlesearch_py

query = "what is programming language"

results = googlesearch_py.search(query)

print(results)
```

Program output:

If results are available for your search query, it will return a list containing dict objects; otherwise, it will return an empty list.
```json
[
    {
        "title": "Programming language - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Programming_language"
    }
...
]
```
