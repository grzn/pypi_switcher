__import__("pkg_resources").declare_namespace(__name__)

import sys
import os
from infi.pyutils.contexts import contextmanager

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


def pars_args():
    """return a valid url or exits"""
    import argparse
    parser = argparse.ArgumentParser(description='configure and apply pipi server on your local workstations', \
                                     usage='usage: set_index_url [-h] --show / url')
    parser.add_argument('url', help='set url to be your system pypi default server', nargs='?')
    parser.add_argument('--show', help='show index url in the relevant config files', action='store_true')
    options = parser.parse_args()
    if options.show:
        show_index_url()
        sys.exit(0)
    else:
        if options.url:
            return options.url
        else:
            parser.print_help()
            print "ERROR:need to specify at list one argument !"
            sys.exit(2)


def verify_url(url):
    from urllib import urlopen
    try:
        urlopen(url)
    except IOError:
        print '{} is not a valid url'.format(url)
        sys.exit(2)

def show_index_url():
    from re import search
    files_list = [item[0] for item in iter_tuples()]
    for filename in files_list:
        filename = os.path.expanduser(filename)
        if os.path.isfile(filename):
            print filename
        else:
            print "{} doesn't exists".format(filename)
            continue
        with open(filename, "r") as fd:
            for line in fd.xreadlines():
                if search("index", line):
                    print line


@contextmanager
def open_configparser_file(filepath, write_on_exit=False):
    parser = ConfigParser()
    if os.path.exists(filepath):
        parser.read(filepath)
    try:
        yield parser
    finally:
        if write_on_exit:
            dirpath = os.path.dirname(filepath)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            with open(filepath, 'w') as fd:
                parser.write(fd)


def set_index_url_in_file(filepath, section_name, key, index_url):
    with open_configparser_file(os.path.expanduser(filepath), True) as pydistutils:
        if not pydistutils.has_section(section_name):
            pydistutils.add_section(section_name)
        pydistutils.set(section_name, key, index_url)


def iter_tuples():
    if os.name == "nt":
        yield ("~/pydistutils.cfg", "easy_install", "index-url")
        yield ("~/pip/pip.ini", "global", "index-url")
    else:
        yield ("~/.pydistutils.cfg", "easy_install", "index-url")
        yield ("~/.pip/pip.conf", "global", "index-url")
    yield("~/.buildout/default.cfg", "buildout", "index")


def set_index_url():
    index_url = pars_args()
    verify_url(index_url)
    for item in iter_tuples():
        filename, section_name, key = item
        set_index_url_in_file( filename, section_name, key, index_url )
