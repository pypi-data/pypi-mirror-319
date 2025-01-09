from setuptools import setup, find_packages

setup(
    name="just_simplify_api",
    version="1.0.0",
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
