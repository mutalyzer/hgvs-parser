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
    (
        'NC_000001(SDHD_v001):', {
            'reference': {
                'id': 'NC_000001',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene transcript',
                'id': 'SDHD',
                'selector': '001'
            }
        }
    ),
    (
        'NC_000001(SDHD_i001):', {
            'reference': {
                'id': 'NC_000001',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene protein',
                'id': 'SDHD',
                'selector': '001'
            }
        }
    ),
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
                'type': 'gene transcript',
                'id': 'MT-TL1',
                'selector': '001'
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_i001):', {
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
    (
        'NC_012920.1(MT-TL1_i001):', {
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
    (
        'NG_012337.1(NM_012459.2):', {
            'reference': {
                'id': 'NG_012337',
                'version': '1',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'accession',
                'id': 'NM_012459',
                'selector': '2'
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_v001):', {
            'reference': {
                'id': 'NG_012337',
                'version': '1',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'gene transcript',
                'id': 'TIMM8B',
                'selector': '001'
            }
        }
    ),
    (
        'LRG_24t1:', {
            'reference': {
                'id': 'LRG_24',
                'type': 'lrg'
            },
            'specific_locus': {
                'type': 'lrg transcript',
                'id': 't1',
            }
        }
    ),
    (
        'LRG_24p1:', {
            'reference': {
                'id': 'LRG_24',
                'type': 'lrg'
            },
            'specific_locus': {
                'type': 'lrg protein',
                'id': 'p1',
            }
        }
    ),
    (
        'NC_000001.1p1:', {
            'reference': {
                'id': 'NC_000001',
                'version': '1',
                'type': 'genbank'
            },
            'specific_locus': {
                'type': 'lrg protein',
                'id': 'p1',
            },
            'notes': ['lrg locus provided for genbank reference']
        }
    ),
    (
        'LRG_24(SDHD):', {
            'reference': {
                'id': 'LRG_24',
                'type': 'lrg'
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
            },
            'notes': ['genbank locus provided for lrg reference']
        }
    ),
]


@pytest.mark.parametrize('description,model', test_cases)
def test_genbank_references(description, model):
    """

    """
    parser = HgvsParser(grammar_path='ebnf/hgvs_mutalyzer_3.g', start_rule='reference')

    assert transform(parser.parse(description)) == model
