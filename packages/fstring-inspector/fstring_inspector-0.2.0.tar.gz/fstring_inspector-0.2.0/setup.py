from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fstring_inspector",
    version="0.2.0",
    author="Yousef Saeed",
    author_email="uosyph@gmail.com",
    description="A tool to analyze and identify issues with f-strings in Python code, ensuring proper formatting, usage, and preventing errors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uosyph/fstring-inspector",
    project_urls={
        "Bug Tracker": "https://github.com/uosyph/fstring-inspector/issues",
        "Documentation": "https://github.com/uosyph/fstring-inspector/blob/main/README.md",
        "Source Code": "https://github.com/uosyph/fstring-inspector",
    },
    packages=find_packages(),
    python_requires=">=3.6",
)
