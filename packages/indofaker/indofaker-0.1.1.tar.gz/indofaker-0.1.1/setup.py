from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="indofaker",  # Nama library di PyPI
    version="0.1.1",  # Versi awal
    author="Firza Aditya",
    author_email="elbuho1315@gmail.com",
    description="A Python library to generate fake data with Indonesian characteristics.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify Markdown format
    url="https://github.com/firzaelbuho/indofaker",  # Link ke repositori GitHub
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
