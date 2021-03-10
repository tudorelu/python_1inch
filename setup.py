import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_1inch", # Replace with your own username
    version="0.0.1",
    author="Tudor Barbulescu",
    author_email="hello@tudorbarbulescu.com",
    description="A python wraper around the 1INCH DEX API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tudorelu/python_1inch",
    project_urls={
        "Bug Tracker": "https://github.com/tudorelu/python_1inch/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)