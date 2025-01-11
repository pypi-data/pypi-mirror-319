from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dmtopython",
    version="0.1.1",
    author="patrickwu123",
    author_email="376023459@qq.com",
    description="大漠插件Python封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickwu123/dmtopython",
    project_urls={
        "Bug Tracker": "https://github.com/patrickwu123/dmtopython/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "dmtopython": ["../types/dmsoft.d.ts"],
    },
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "pywin32>=228",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
    },
) 