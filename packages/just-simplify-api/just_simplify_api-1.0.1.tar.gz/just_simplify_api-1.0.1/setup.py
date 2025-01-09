from setuptools import setup, find_packages

# Read the README file
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="just_simplify_api",
    version="1.0.1",
    packages=find_packages(),
    description="Mesh API tools for consistent response formatting and validation",
    author="Preston Hollis",
    author_email="thomas.preston.hollis@gmail.com",
    url="https://github.com/tphollis/api-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
