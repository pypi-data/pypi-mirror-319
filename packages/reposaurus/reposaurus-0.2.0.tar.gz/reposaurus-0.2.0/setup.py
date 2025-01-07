from setuptools import setup, find_packages
import codecs

# Read long description with proper encoding
with codecs.open("README.md", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name="reposaurus",
    version="0.2.0",  # Updated for new feature
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'reposaurus=reposaurus.cli.main:main',
        ],
    },
    install_requires=[
        'pathspec>=0.9.0',  # For gitignore-style pattern matching
        'chardet>=5.0.0',   # For file encoding detection
        'pyyaml>=6.0.1',    # For configuration and output handling
    ],
    author="Andy Thomas",
    author_email="your.email@example.com",
    description="A powerful tool for transforming repositories into text files and detecting sensitive information innit...🦖",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reposaurus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
)
