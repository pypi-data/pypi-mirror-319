from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='selenium_driver_initializer', # name of pack which will be package dir below project
    version='0.0.1',
    url='https://github.com/ZeeshanAhmed95/selenium-driver-initializerPKG',
    author='Zeeshan Ahmed',
    author_email='zeeshanaliahmed@gmail.com',
    description='A Python package to initialize Selenium WebDriver with custom configurations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["selenium","requests"],
)
