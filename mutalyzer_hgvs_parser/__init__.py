"""
mutalyzer_hgvs_parser: Parser for HGVS variant descriptions.


Copyright (c) 2019 Leiden University Medical Center <humgen@lumc.nl>
Copyright (c) 2019 Mihai Lefter <m.lefter@lumc.nl>


...
"""
from configparser import ConfigParser
from os.path import dirname, abspath

from .mutalyzer_hgvs_parser import parse_description,\
    parse_description_to_model


config = ConfigParser()
config.read_file(open('{}/setup.cfg'.format(dirname(abspath(__file__)))))

_copyright_notice = 'Copyright (c) {} {} <{}>'.format(
    config.get('metadata', 'copyright'),
    config.get('metadata', 'author'),
    config.get('metadata', 'author_email'))

usage = [config.get('metadata', 'description'), _copyright_notice]


def doc_split(func):
    return func.__doc__.split('\n\n')[0]


def version(name):
    return '{} version {}\n\n{}\nHomepage: {}'.format(
        config.get('metadata', 'name'),
        config.get('metadata', 'version'),
        _copyright_notice,
        config.get('metadata', 'url'))
