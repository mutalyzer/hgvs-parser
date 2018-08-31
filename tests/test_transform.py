"""
Checking the lark tree transformation.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.transform import transform, get_variants, get_reference_information


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

    assert get_reference_information(parser.parse(description)) == model


test_variants = [
    # # No change
    # (
    #     '=',
    #     # The entire reference sequence was analysed and no change was identified.
    #     {
    #
    #     }
    # ),
    # (
    #     '123=',
    #     # A screen was performed showing that nucleotide 123 was not changed.
    #     {
    #
    #     }
    # ),
    # Substitutions
    (
        '100C>A',
        {
            'variants': [
                {
                    'substitution': {
                        'location': {
                            'position': 100
                        },
                        'inserted': [
                            {
                                'sequence': 'A',
                                'source': 'description'
                            }
                        ],
                        'deleted': [
                            {
                                'sequence': 'C',
                                'source': 'description'
                            }
                        ]
                    }
                }
            ]
        }
    ),
    (
        '100+3C>A',
        {
            'variants': [
                {
                    'substitution': {
                        'location': {
                            'position': 100,
                            'offset': 3
                        },
                        'inserted': [
                            {
                                'sequence': 'A',
                                'source': 'description'
                            }
                        ],
                        'deleted': [
                            {
                                'sequence': 'C',
                                'source': 'description'
                            }
                        ]
                    }
                }
            ]
        }
    ),
    (
        '*100C>A',
        {
            'variants': [
                {
                    'substitution': {
                        'location': {
                            'outside_translation': 'upstream',
                            'position': 100
                        },
                        'inserted': [
                            {
                                'sequence': 'A',
                                'source': 'description'
                            }
                        ],
                        'deleted': [
                            {
                                'sequence': 'C',
                                'source': 'description'
                            }
                        ]
                    }
                }
            ]
        }
    ),
    (
        '*1-3C>A',
        {
            'variants': [
                {
                    'substitution': {
                        'location': {
                            'outside_translation': 'upstream',
                            'offset': -3,
                            'position': 1
                        },
                        'inserted': [
                            {
                                'source': 'description',
                                'sequence': 'A'
                            }
                        ],
                        'deleted': [
                            {
                                'source': 'description',
                                'sequence': 'C'
                            }
                        ]
                    }
                }
            ]
        }
    ),
    (
        '-1+3C>A',
        {
            'variants': [
                {
                    'substitution': {
                        'location': {
                            'outside_translation': 'downstream',
                            'offset': 3,
                            'position': 1
                        },
                        'inserted': [
                            {
                                'source': 'description',
                                'sequence': 'A'
                            }
                        ],
                        'deleted': [
                            {
                                'source': 'description',
                                'sequence': 'C'
                            }
                        ]
                    }
                }
            ]
        }
    ),
    # (
    #     '-401C>T',
    #     {
    #
    #     }
    # ),
    # (
    #     '93+1G>T',
    #     {
    #
    #     }
    # ),
    # # Deletions
    # (
    #     '19del',
    #     {
    #
    #     }
    # ),
    # (
    #     '704+1del',
    #     {
    #
    #     }
    # ),
    # (
    #     '19_21del',
    #     {
    #
    #     }
    # ),
    # (
    #     '183_186+48del',
    #     # From NG_012232.1(NM_004006.1):c.183_186+48del a deletion of
    #     # nucleotides 183 to 186+48 (coding DNA reference sequence), crossing
    #     # an exon/intron border.
    #     {
    #
    #     }
    # ),
    # (
    #     '4072-1234_5155-246del',
    #     # From NG_012232.1(NM_004006.1):c.4072-1234_5155-246del
    #     {
    #
    #     }
    # ),
    # (
    #     '(4071+1_4072-1)_(5154+1_5155-1)del',
    #     # From NG_012232.1(NM_004006.1):c.(4071+1_4072-1)_(5154+1_5155-1)del
    #     {
    #
    #     }
    # ),
    # (
    #     '(?_-245)_(31+1_32-1)del',
    #     {
    #
    #     }
    # ),
    # (
    #     '(?_-1)_(*1_?)del',
    #     {
    #
    #     }
    # ),
    # # Duplications
    # (
    #     '20dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '1704+1dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '20_23dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '260_264+48dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '4072-1234_5155-246dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '(4071+1_4072-1)_(5154+1_5155-1)dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '(?_-127)_(31+1_32-1)dup',
    #     {
    #
    #     }
    # ),
    # (
    #     '(?_-1)_(*1_?)dup',
    #     {
    #
    #     }
    # ),
    # # Insertions
    # (
    #     '32867861_32867862insT',
    #     {
    #
    #     }
    # ),
    # # Mosaic cases.
    # (
    #     '85=/T>C',
    #     {
    #
    #     }
    # ),
    # (
    #     '19_21=/del',
    #     {
    #
    #     }
    # ),
    # (
    #     '19_21=/dup',
    #     {
    #
    #     }
    # ),
    # # Chimeric cases.
    # (
    #     '85=//T>C',
    #     {
    #
    #     }
    # ),
    # (
    #     '19_21=//del',
    #     {
    #
    #     }
    # ),
    # (
    #     '19_21=//dup',
    #     {
    #
    #     }
    # ),

]


@pytest.mark.parametrize('description,model', test_variants)
def test_variants(description, model):
    parser = HgvsParser(grammar_path='ebnf/hgvs_mutalyzer_3.g', start_rule='variants')

    assert get_variants(parser.parse(description)) == model
