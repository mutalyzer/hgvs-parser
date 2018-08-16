"""
Checking the lark tree transformation.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.transform import transform


test_cases = [
    # genbank references
    (
        'NC_000001:', {
            'reference': {
                'id': 'NC_000001',
                'type': 'genbank'
            }
        }
    ),
    (
        'NC_000001.10:', {
            'reference': {
                'id': 'NC_000001',
                'version': '10',
                'type': 'genbank'
            }
        }
    ),
    (
        'LRG_1:', {
            'reference': {
                'id': 'LRG_1',
                'type': 'lrg'
            }
        }
    ),
    (
        'LRG_1.1:', {
            'reference': {
                'id': 'LRG_1',
                'version': '1'
            },
            'notes': ['version supplied for LRG reference']
        }
    ),
    (
        'NC_000001(SDHD):', {
            'reference': {
                'id': 'NC_000001',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD'
            }
        }
    ),
    # Problem with the following since it is interpreted as an accession and
    # not as a genename, since it doesn't have a version and neither a '-'.
    # (
    #     'NC_000001(SDHD_v001):', {
    #         'reference': {
    #             'id': 'NC_000001',
    #             'type': 'genbank'
    #         },
    #         'specific_locus': {
    #             'type': 'gene transcript',
    #             'id': 'SDHD',
    #             'selector': '001'
    #         }
    #     }
    # ),
    # (
    #     'NC_000001(SDHD_i001):', {
    #         'reference': {
    #             'id': 'NC_000001',
    #             'type': 'genbank'
    #         },
    #         'specific_locus': {
    #             'type': 'gene protein',
    #             'id': 'SDHD',
    #             'selector': '001'
    #         }
    #     }
    # ),
    (
        'NC_012920.1(MT-TL1):', {
            'reference': {
                'id': 'NC_012920',
                'version': '1',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1'
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_v001):', {
            'reference': {
                'id': 'NC_012920',
                'version': '1',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene protein',
                'id': 'MT-TL1',
                'selector': '001'
            }
        }
    ),
]


@pytest.mark.parametrize('description,model', test_cases)
def test_genbank_references(description, model):
    """

    """
    parser = HgvsParser(grammar_path='ebnf/hgvs_mutalyzer_3.g', start_rule='reference')

    assert transform(parser.parse(description)) == model
