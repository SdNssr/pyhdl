import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyhdl",
    version = "0.1.0",
    description = ("A simpe HDL for learning hardware design."),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 2.7',
        "License :: Other/Proprietary License",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords = "hdl hardware design simple",
    author = "Saad Nasser",
    license = "Proprietary",
    packages=['pyhdl'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
