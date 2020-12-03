from setuptools import setup, find_packages

setup(
    name='abstractor',
    version='4.1.1',
    description='Abstraction generator for AskOmics, from a distant SPARQL endpoint',
    author='Xavier Garnier',
    author_email='xavier.garnier@irisa.fr',
    url='https://github.com/askomics/abstractor',
    download_url='https://github.com/askomics/abstractor/archive/4.1.1.tar.gz',
    install_requires=['SPARQLWrapper'],
    packages=find_packages(),
    license='AGPL',
    platforms='Posix; MacOS X; Windows',
    scripts=['abstractor'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ])
