from setuptools import setup, find_packages

# Read the README file
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="just_simplify_api",
    version="1.0.2",
    packages=find_packages(),
    description="API tools for consistent response formatting and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Preston Hollis",
    author_email="thomas.preston.hollis@gmail.com",
    url="https://github.com/tphollis/api-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
