#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

test_requirements = [ ]

setup(
    author="Jhonny Jiménez",
    author_email='MasterChampionLigue@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nodeeditor',
    name='nodeeditor',
    # packages=find_packages(include=['_template', '_template.*']),
    packages=find_packages(include=['nodeeditor*'], exclude=['examples*', 'test*']),
    package_data={'': ['qss/*']},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JhonnyJimenez/template',
    version='0.9.0',
    zip_safe=False,
)
