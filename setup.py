#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='treadmill_tracking',
    version='0.0.0',
    description='Datajoint pipeline for treadmill tracking, extending the core electrophysiology pipeline of the Moser Lab',
    author='Vathes',
    author_email='support@vathes.com',
    license='MIT',
    url='https://github.com/kavli-ntnu/project-treadmill',
    packages=find_packages(exclude=[]),
    install_requires=requirements,
    python_requires='>=3.6'
)
