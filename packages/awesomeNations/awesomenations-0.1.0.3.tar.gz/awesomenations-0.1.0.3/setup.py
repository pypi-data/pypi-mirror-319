from setuptools import setup, find_packages

def long_description() -> str:
    long_description: str = ''
    with open('README.md', 'r', encoding='utf-8') as file:
        long_description += file.read()
    with open('CHANGELOG.md', 'r', encoding='utf-8') as file:
        long_description += f'\n\n{file.read()}'
    return long_description

setup(
    name='awesomeNations',
    version='0.1.0.3',
    description='A simple python web scraping library for NationStates',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Orly Neto',
    author_email='orly2carvalhoneto@gmail.com',
    license='MIT License',
    keywords=['NationStates', 'Scrapper', 'Web Scrapper', 'NationStates scrapper'],
    packages=find_packages(),
    install_requires=['beautifulsoup4==4.12.3', 'requests==2.32.3', 'selenium==4.27.1', 'webdriver-manager==4.0.2', 'lxml==5.3.0'])