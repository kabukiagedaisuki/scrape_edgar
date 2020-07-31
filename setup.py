from setuptools import find_packages, setup

setup (
    name         = "scrape_edgar",
    version      = "0.0.1",
    entry_points = {
        "console_scripts" : [ "scrape_edgar = scrape_edgar.__main__:main" ],
    }
)
