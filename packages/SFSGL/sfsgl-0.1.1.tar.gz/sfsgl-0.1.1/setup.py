
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    author='Hasan Ali Özkan',
    description='Simple File Sharing and Gathering Library',
    name='SFSGL',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['flask', 'werkzeug'],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
)