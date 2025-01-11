from setuptools import setup

libs = open("requirements.txt").read().splitlines()
setup(
    name="nm25",
    version="1.0",
    url="",
    license="MIT",
    author="",
    author_email="",
    platforms=["any"],
    package_data={
        "nm25": ["data/*.py", "data/*.md"],
    },
)
