"""
Checking the lark tree transformation.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.to_model import parse_tree_to_model, get_variants, get_reference_information


test_cases = [
    # No specific locus
    # - genbank reference with no version
    (            # print("parse_tree")

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
                    'type': 'substitution',
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
            ]
        }
    ),
    (
        '100+3C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
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
            ]
        }
    ),
    (
        '*100C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'location': {
                        'position': 100,
                        'outside_translation': 'upstream'
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
            ]
        }
    ),
    (
        '*1-3C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'location': {
                        'position': 1,
                        'offset': -3,
                        'outside_translation': 'upstream'
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
            ]
        }
    ),
    (
        '-1+3C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'location': {
                        'position': 1,
                        'offset': 3,
                        'outside_translation': 'downstream'
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
            ]
        }
    ),
    # Deletions
    (
        '10del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'position': 10,
                    },
                }
            ]
        }
    ),
    (
        # Note: the addition of 'A' is not HGVS.
        '10delA',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'position': 10,
                    },
                    'deleted': [
                        {
                            'sequence': 'A',
                            'source': 'description'
                        }
                    ],
                }
            ]
        }
    ),
    (
        '100+1del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'position': 100,
                        'offset': 1,
                    },
                }
            ]
        }
    ),
    (
        '10_20del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'position': 10,
                        },
                        'end': {
                            'position': 20,
                        }
                    },
                }
            ]
        }
    ),
    (
        '10-1_20-3del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'position': 10,
                            'offset': -1
                        },
                        'end': {
                            'position': 20,
                            'offset': -3
                        }
                    },
                }
            ]
        }
    ),
    (
        # Note: the addition of '5' is not HGVS.
        '10_15del5',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'position': 10,
                        },
                        'end': {
                            'position': 15,
                        }
                    },
                    'deleted': [
                        {
                            'source': 'description',
                            'length': 5
                        }
                    ],
                }
            ]
        }
    ),
    (
        '(10_20)_30del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'uncertain': {
                                'start': {
                                    'position': 10,
                                },
                                'end': {
                                    'position': 20,
                                }
                            },
                        },
                        'end': {
                            'position': 30,
                        }
                    },
                }
            ]
        }
    ),
    (
        '(10_20)_(30_40)del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'uncertain': {
                                'start': {
                                    'position': 10,
                                },
                                'end': {
                                    'position': 20,
                                }
                            },
                        },
                        'end': {
                            'uncertain': {
                                'start': {
                                    'position': 30,
                                },
                                'end': {
                                    'position': 40,
                                }
                            },
                        }
                    },
                }
            ]
        }
    ),
    (
        '(?_-20)_(30+1_30-1)del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'uncertain': {
                                'start': {
                                    'position': '?',
                                },
                                'end': {
                                    'position': 20,
                                    'outside_translation': 'downstream',
                                }
                            },
                        },
                        'end': {
                            'uncertain': {
                                'start': {
                                    'position': 30,
                                    'offset': 1,
                                },
                                'end': {
                                    'position': 30,
                                    'offset': -1,
                                }
                            },
                        }
                    },
                }
            ]
        }
    ),
    (
        '(?_-1)_(*1_?)del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'start': {
                            'uncertain': {
                                'start': {
                                    'position': '?',
                                },
                                'end': {
                                    'position': 1,
                                    'outside_translation': 'downstream',
                                }
                            },
                        },
                        'end': {
                            'uncertain': {
                                'start': {
                                    'position': 1,
                                    'outside_translation': 'upstream',
                                },
                                'end': {
                                    'position': '?',
                                }
                            },
                        }
                    },
                }
            ]
        }
    ),
    # Duplications
    (
        '10dup',
        {
            'variants': [
                {
                    'type': 'dup',
                    'location': {
                        'position': 10,
                    },
                }
            ]
        }
    ),
    # (
    #     '260_264+48dup',
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
    # Insertions
    (
        '11_12insT',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12ins[T]',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12ins[T;10_20]',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T'
                        },
                        {
                            'location': {
                                'start': {
                                    'position': 10
                                },
                                'end': {
                                    'position': 20
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12ins[T;10_20inv]',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T'
                        },
                        {
                            'location': {
                                'start': {
                                    'position': 10
                                },
                                'end': {
                                    'position': 20
                                }
                            },
                            'inverted': 'inv'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12ins[T;10_20inv;NM_000001.1:c.100_200]',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T'
                        },
                        {
                            'location': {
                                'start': {
                                    'position': 10
                                },
                                'end': {
                                    'position': 20
                                }
                            },
                            'inverted': 'inv'
                        },
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1'
                                },
                                'coordinate': 'c',
                                'location': {
                                    'start': {
                                        'position': 100
                                    },
                                    'end': {
                                        'position': 200
                                    }
                                },
                            }
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12insNM_000001.1:c.100_200',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1'
                                },
                                'coordinate': 'c',
                                'location': {
                                    'start': {
                                        'position': 100
                                    },
                                    'end': {
                                        'position': 200
                                    }
                                },
                            }
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12insNM_000001.1',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                    'insertions': [
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1'
                                },
                            }
                        }
                    ]
                }
            ]
        }
    ),
    # Inversions
    (
        '11_12inv',
        {
            'variants': [
                {
                    'type': 'inv',
                    'location': {
                        'start': {
                            'position': 11,
                        },
                        'end': {
                            'position': 12,
                        }
                    },
                }
            ]
        }
    ),
    # Conversions
    (
        '10_20con30_40',
        {
            'variants': [
                {
                    'type': 'con',
                    'location': {
                        'start': {
                            'position': 10,
                        },
                        'end': {
                            'position': 20,
                        }
                    },
                    'insertions': [
                        {
                            'location': {
                                'start': {
                                    'position': 30,
                                },
                                'end': {
                                    'position': 40,
                                }
                            },
                        }
                    ]
                }
            ]
        }
    ),
    # Deletion-insertions
    (
        '10delinsGA',
        {
            'variants': [
                {
                    'type': 'delins',
                    'location': {
                        'position': 10,
                    },
                    'insertions': [
                        {
                            'sequence': 'GA'
                        }
                    ]
                }
            ]
        }
    ),
    # Deletion-insertions
    (
        '10delinsGA',
        {
            'variants': [
                {
                    'type': 'delins',
                    'location': {
                        'position': 10,
                    },
                    'insertions': [
                        {
                            'sequence': 'GA'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '10_20delinsGA',
        {
            'variants': [
                {
                    'type': 'delins',
                    'location': {
                        'start': {
                            'position': 10,
                        },
                        'end': {
                            'position': 20,
                        },
                    },
                    'insertions': [
                        {
                            'sequence': 'GA'
                        }
                    ]
                }
            ]
        }
    ),
    # Repeats
    # (
    #     '10GA[20]',
    #     {
    #         'variants': [
    #             {
    #                 'type': 'repeat',
    #                 'location': {
    #                     'position': 10,
    #                 },
    #                 'insertions': [
    #                     {
    #                         'sequence': 'GA',
    #                         'length': 4
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ),
    # (
    #     '123_191CAG[19]CAA[4]',
    #     {
    #         'variants': [
    #             {
    #                 'type': 'repeat',
    #                 'location': {
    #                     'start': {
    #                         'position': 123,
    #                     },
    #                     'end': {
    #                         'position': 191,
    #
    #                     }
    #                 },
    #                 'insertions': [
    #                     {
    #                         'sequence': 'CAG',
    #                         'length': 19
    #                     },
    #                     {
    #                         'sequence': 'CAA',
    #                         'length': 4
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ),

    # No changes (equal)
    # TODO: Should we enforce exact positions for the range?
    (
        '10=',
        {
            'variants': [
                {
                    'type': 'equal',
                    'location': {
                        'position': 10
                        }
                }
            ]
        }
    ),
    (
        '10_20=',
        {
            'variants': [
                {
                    'type': 'equal',
                    'location': {
                        'start': {
                            'position': 10,
                        },
                        'end': {
                            'position': 20,
                        }
                    },
                }
            ]
        }
    ),
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
