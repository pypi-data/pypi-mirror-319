from os import path

from setuptools import find_packages, setup

working_directory = path.dirname(path.abspath(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="streamlit-donut",
    version="0.1.3",
    author="Benson Nderitu",
    author_email="bent25066@gmail.com",
    description="A Streamlit component for rendering donut metrics/visuals",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benson-nderitu/streamlit-donut",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
