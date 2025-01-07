from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dmtopython",
    version="0.1.0",
    author="nan1989",
    author_email="your.email@example.com",
    description="大漠插件Python API封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nan1989/dmtopython",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pywin32>=228",
    ],
) 