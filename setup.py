from setuptools import setup, find_packages

setup(
    name='mocanexion',
    version='1.1.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    url='https://github.com/chainreaktive/mocanexion',
    license='The Unlicense',
    author='Nick Saway',
    author_email='nick.saway@chainreaktive.com',
    description='A Python connection to MOCA',
    keywords='moca wms',
    install_requires=['pandas', 'requests'],
    python_requires='>=3'
)
