.. _installation:

Installation
============

PyHDL supports Python 2.7, and Python 3.3 and up.

The best method to install PyHDL is in a virtualenv.

virtualenv
----------

Virtualenv is a way to run multiple side-by-side versions of Python, one for each project.
If you use Python for other projects, this prevents conflicting dependencies.

To install virtualenv, use::

    $ sudo pip install virtualenv 

Once you have installed virtualenv, open up a shell and create a new environment::

    $ mkdir myproject
    $ cd myproject
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing distribute............done.

Now, whenever you want to work on a project, you have to activate the corresponding environment::

    $ . venv/bin/activate

You should now be using your virtualenv (your shell prompt probably changed to show the active environment).

Now you can install PyHDL by running this command::

    $ pip install pyhdl

You are ready to go now! Head over to the :ref:`quickstart` to get started.

System wide installation
------------------------

This is another option, though it is not recommended. Run pip with root privileges::

    $ sudo pip install Flask

Living on the Edge
------------------

If you want to run the latest version of PyHDL, you can checkout the git repo directly.

Just do this in a new virtualenv::
    
    $ git clone https://github.com/SdNssr/pyhdl.git
    $ cd pyhdl
    $ virtualenv venv --distribute
    New python executable in venv/bin/python
    Installing distribute............done.
    $ . venv/bin/activate
    $ python setup.py develop
    ...
    Finished processing dependencies for pyhdl
