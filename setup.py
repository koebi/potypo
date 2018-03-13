# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='potypo',
    version='0.0.1',
    description='spellchecking for .po-files',
    long_description=long_description,
    url='https://github.com/koebi/potypo',
    author='Jakob Schnell',
    author_email='potypo@ezelo.de',  # Optional
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='setuptools development spellcheck translation typo gettext',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pyenchant','polib'],
    entry_points={
        'console_scripts': [
            'potypo=potypo.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/koebi/potypo/issues',
        'Source': 'https://github.com/koebi/potypo/',
    },
)
