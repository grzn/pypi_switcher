Overview
========
This repository is just a skeleton we use for projects.

Usage
-----
Nothing to use here.

Checking out the code
=====================

This project uses buildout, and git to generate `setup.py` and `__version__.py`.
In order to generate these, run:

    python -S bootstrap.py -t
    bin/buildout buildout:develop= install setup.py __version__.py
    python setup.py develop

In our development environment, we use isolated python builds, by running the following instead of the last command:

    bin/buildout install development-scripts

