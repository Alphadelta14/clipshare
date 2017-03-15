#!/usr/bin/env python
"""
moopaste

Author: Alphadelta14
"""

from setuptools import setup, find_packages

__version__ = '0.1.0'  # Overwritten below
execfile('moopaste/version.py')  # pylint: disable=exec-used

setup(
    name='moopaste',
    version=__version__,
    description='Easily share screenshots and code snippets',
    url='https://github.com/Alphadelta14/moopaste',
    author='Alphadelta14',
    author_email='alpha@alphaservcomputing.solutions',
    license='MIT',
    install_requires=[],
    entry_points={
        'console_scripts': [],
        'distutils.commands': [],
    },
    scripts=[
        'bin/moopaste',
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ]
)
