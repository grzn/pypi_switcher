__import__("pkg_resources").declare_namespace(__name__)

from sys import argv
from infi.pyutils.contexts import contextmanager
from os import path, makedirs


@contextmanager
def open_configparser_file(filepath, write_on_exit=False):
    from ConfigParser import ConfigParser
    parser = ConfigParser()
    if path.exists(filepath):
        parser.read(filepath)
    try:
        yield parser
    finally:
        if write_on_exit:
            dirpath = path.dirname(filepath)
            if not path.exists(dirpath):
                makedirs(dirpath)
            with open(filepath, 'w') as fd:
                parser.write(fd)


def set_index_url_in_file(filepath, section_name, key, index_url):
    with open_configparser_file(path.expanduser(filepath), True) as pydistutils:
        if not pydistutils.has_section(section_name):
            pydistutils.add_section(section_name)
        pydistutils.set(section_name, key, index_url)

def set_index_url(argv=argv[1:]):
    [index_url] = argv
    set_index_url_in_file("~/.pydistutils.cfg", "easy_install", "index-url", index_url)
    set_index_url_in_file("~/.pip/pip.conf", "global", "index-url", index_url)
    set_index_url_in_file("~/.buildout/default.cfg", "buildout", "index", index_url)

