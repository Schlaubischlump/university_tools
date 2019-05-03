"""
setup.py to 'build', 'install'
Usage: python setup.py 'command'
"""
from setuptools import setup

setup(
    name='universitytools',
    version='0.1.0',
    author='SchlaubiSchlump',
    packages=['universitytools'],
    license='GPLv3+',
    scripts=['bin/fahrplan', 'bin/mensa'],
    long_description=open('Readme.md').read(),
    install_requires=['texttable'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries'
        'Topic :: Utilities'
    ],
    keywords='fahrplan mensa mainz uni jgu',
)
