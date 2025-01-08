from setuptools import setup, find_packages

setup(
    name="text_format_converter",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Ran Geler",
    author_email="geler.ran@gmail.com",
    description="text format converter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dataran/TextFormatConverter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)