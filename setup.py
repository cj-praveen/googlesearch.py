import setuptools

setuptools.setup(
    name="googlesearch.py",
    version="1.6.1",
    description="The Google search scraper for the Python programming language.",
    author="CJ Praveen",
    url="https://github.com/cj-praveen/googlesearch.py",
    long_description=str(open("README.md", "r", encoding="utf-8").read()),
    long_description_content_type="text/markdown",
    keywords="googlesearch.py, python google search, google search pypi, google api",
    package_dir={"": "src"},
    install_requires=["httpx"]
)