from setuptools import setup

with open("README.md","r",encoding="utf-8") as f:
    long_description = f.read()

REPO_NAME = "Hybrid-Recommender-Using-Machine-Learning"
AUTHOR_NAME = "Mithun Vandhinika"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = "0.0.1",
    author = AUTHOR_NAME,
    description="A small package for the Hybrid recommender system",
    long_description = long_description,
    long_description_content_type="text/markdown",
    author_email = "mithun18005@gmail.com",
    packages=[SRC_REPO],
    license = "MIT",
    python_requires = ">3.7",
    install_requires=LIST_OF_REQUIREMENTS
)