from setuptools import setup, find_packages

setup(
    name="scraper_sanskrit",  # Package name
    version="0.2.0",          # Initial version
    description="A web scraper for Sanskrit dictionary results using Selenium and BeautifulSoup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jagruti",
    # author_email="your.email@example.com",
    # url="https://github.com/yourusername/sanskrit_scraper",  # Replace with your repo
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "webdriver-manager",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
