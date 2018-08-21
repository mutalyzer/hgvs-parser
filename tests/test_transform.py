"""
Checking the lark tree transformation.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.transform import transform


test_cases = [
    # No specific locus
    # - genbank reference with no version
    (
        'NC_000001:', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            }
        }
    ),
    # - genbank reference with accession and version
    (
        'NC_000001.10:', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '10',
            }
        }
    ),
    # - lrg reference
    (
        'LRG_1:', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_1',
            }
        }
    ),
    # - lrg reference with version - should not be possible
    (
        'LRG_1.1:', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_1',
                'version': '1',
            },
            'notes': ['version supplied for LRG reference']
        }
    ),
    # Specific locus present
    # - with gene names only
    (
        'NC_000001(SDHD):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_012920',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1',
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'TIMM8B',
            }
        }
    ),
    (
        'NC_000001(SDHD_v001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
                'transcript variant': '001',
            }
        }
    ),
    (
        'NC_000001(SDHD_i001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
                'protein isoform': '001',
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_v001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'TIMM8B',
                'transcript variant': '001'
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_i001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'TIMM8B',
                'protein isoform': '001'
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_v001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_012920',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1',
                'transcript variant': '001',
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_i001):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_012920',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1',
                'protein isoform': '001',
            }
        }
    ),
    # - with accession and version
    (
        'NG_012337.1(NM_012459.2):', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'accession',
                'accession': 'NM_012459',
                'version': '2',
            }
        }
    ),
    # - LRG ones
    (
        'LRG_24t1:', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_24',
            },
            'specific_locus': {
                'type': 'lrg transcript',
                'transcript variant': 't1',
            }
        }
    ),
    (
        'LRG_24p1:', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_24',
            },
            'specific_locus': {
                'type': 'lrg protein',
                'protein isoform': 'p1',
            }
        }
    ),
    # - mix
    (
        'NC_000001.1t1:', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '1',
            },
            'specific_locus': {
                'type': 'lrg transcript',
                'transcript variant': 't1',
            },
            'notes': ['lrg locus provided for genbank reference']
        }
    ),
    (
        'NC_000001.1p1:', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '1',
            },
            'specific_locus': {
                'type': 'lrg protein',
                'protein isoform': 'p1',
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
def test_reference_part(description, model):
    """

    """
    parser = HgvsParser(grammar_path='ebnf/hgvs_mutalyzer_3.g', start_rule='reference')

    assert transform(parser.parse(description)) == model
