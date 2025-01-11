from setuptools import setup

libs = open("requirements.txt").read().splitlines()
setup(
    name="nm25",
    version="1.4",
    url="",
    license="MIT",
    author="",
    author_email="",
    platforms=["any"],
    package_data={
        "nm25": ["data/th/*.md"],
    },
)
