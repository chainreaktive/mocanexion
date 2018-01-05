from distutils.core import setup

setup(
    name='mocanexion',
    version='1.0.2',
    packages=['mocanexion'],
    url='https://github.com/rnsaway/mocanexion',
    license='The Unlicense',
    author='Nick Saway',
    author_email='rnsaway@gmail.com',
    description='A python connection to MOCA',
    keywords='moca wms',
    install_requires=['pandas', 'requests'],
    python_requires='>=3'
)