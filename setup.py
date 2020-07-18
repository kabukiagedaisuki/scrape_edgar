from setuptools import find_packages, setup

setup (
    name         = "edgar",
    version      = "0.0.1",
    entry_points = {
        "console_scripts" : [ "edgar = edgar.__main__:main" ],
    }
)
