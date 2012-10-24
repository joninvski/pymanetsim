#!/usr/bin/env python
"""Distutils based setup script for Sympy.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command (you'll probably need root privileges for that):

    python setup.py install

This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:

    python setup.py --help install

    In addition, there are some other commands:

    python setup.py clean -> will clean all trash (*.pyc and stuff)
    python setup.py test  -> will run the complete test suite
    python setup.py gen_doc -> generates the manual

To get a full list of avaiable commands, read the output of:

    python setup.py --help-commands

Or, if all else fails, feel free to write to the sympy list at
sympy@googlegroups.com and ask for help.
"""

from distutils.core import setup
from distutils.core import Command
import sys, os

# Make sure I have the right Python version.
if sys.version_info[1] < 6:
    print("PyManetSim requires Python 2.6 or newer. Python %d.%d detected" % \
          sys.version_info[:2])
    sys.exit(-1)

# Check that this list is uptodate against the result of the command (you can
# omit the thirdparty/ dir):
# $ find * -name __init__.py |sort
modules = [
    'pymanetsim',
    'pymanetsim/jobs',
    'pymanetsim/protocols/bfg',
    'pymanetsim/protocols/dsr',
    'pymanetsim/protocols',
    'pymanetsim/protocols/simple_and_direct',
    'pymanetsim/unit_tests',
]

class clean(Command):
    """Cleans *.pyc and debian trashs, so you should get the same copy as
    is in the svn.
    """

    description = "Clean everything"
    user_options = [("all","a","the same")]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        os.system("python manage.py -c")
        os.system("rm -f python-build-stamp-2.4")
        os.system("rm -f MANIFEST")
        os.system("rm -rf build")
        os.system("rm -rf dist")

class gen_doc(Command):
    """Generate the (html) api documentation using epydoc

    output is sent to the directory ../api/
    """

    description = "generate the api doc"
    user_options = []

    target_dir = "../api/"

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        os.system("python pymanetsim/manage.py --make-manual")

class test_pymanetsim(Command):
    """
    Runs the tests of pymanetsim
    """

    def __init__(self, ):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        pass

setup(
    name = 'pymanetsim',
    version = '0.1-alpha',
    description = 'Python Manet Simulator',
    author = 'Joao Trindade',
    author_email='jtrindade@tagus.inesc-id.pt',
    license = 'GPL',
    url = 'Don\'t know yet',
    packages = ['pymanetsim'] + modules,
    scripts = [],
    ext_modules = [],
    package_data = { 'sympy.utilities.mathml' : ['data/*.xsl'] },
    data_files = [('share/man/man1', ['doc/man/isympy.1'])],
    cmdclass    = {
        'test': test_pymanetsim,
        'gen_doc' : gen_doc,
        'clean' : clean,
    },
)


