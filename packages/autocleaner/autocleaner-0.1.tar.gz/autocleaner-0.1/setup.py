# setup.py
from setuptools import setup, find_packages

setup(
    name='autocleaner',            # Name of the package
    version='0.1',                 # Version of the package
    packages=find_packages(),      # Automatically find package directories
    install_requires=[],           # List dependencies if any
    long_description=open('README.md').read(),  # Package description
    long_description_content_type='text/markdown',  # Readme file format
    author='Mukilan M',            # Author name
    
    description='auto cleaning the data with easy user interface',  # Short description
    
)
