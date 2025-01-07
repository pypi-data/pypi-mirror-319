# setup.py

from setuptools import setup, find_packages
import os

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dre_datamanager',  # Changed to a unique name to avoid conflicts
    version='0.1.0',
    author='George Graves',
    author_email='george.graves@centaurihs.com',
    description='A package for managing data operations using PySpark',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_datamanager',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',  # Adjust as needed
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pyspark>=3.0.0',
        # Add other dependencies if needed
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            # Add other development dependencies if needed
        ]
    },
)
