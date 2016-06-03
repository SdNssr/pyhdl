"""
PyHDL
-----
A simple HDL written in Python.
"""

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyhdl",
    version="0.3.0",
    description=("A simpe HDL for learning hardware design."),
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords="hdl hardware design simple",
    author="Saad Nasser",
    author_email="SdNssr@users.noreply.github.com",
    url="https://github.com/SdNssr/pyhdl",
    license="MIT",
    packages=['pyhdl'],
    install_requires=[
        'six==1.10.0'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
