# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="authorai",
    version='0.2.2',
    description='Enhance your creative authoring flow, leave the plumbing to AuthorAI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.authorai.org",
    keywords = "AI generative transformer authoring automation",
    author='AuthorAi.org',
    author_email='authorai.org@gmail.com',
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],    
    packages=["authorai"],
    include_package_data=True,
    install_requires=['openai', 'bs4', 'markdownify', 'urllib3', 'stability_sdk'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)