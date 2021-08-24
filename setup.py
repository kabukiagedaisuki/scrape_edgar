from setuptools import find_packages, setup

setup (
    name         = "scrape_edgar",
    version      = "0.0.1",
    packages     = find_packages(),
    install_requires=['click', 'numpy', 'matplotlib', 'selenium'],
    entry_points = {
        "console_scripts" : [ "scrape_edgar = scrape_edgar.__main__:main" ],
    }
)
