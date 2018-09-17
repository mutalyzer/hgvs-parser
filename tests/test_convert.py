"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.to_model import parse_tree_to_model


REFERENCES = [
    # No specific locus
    # - genbank reference with no version
    (

        'NC_000001', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            }
        }
    ),
    # - genbank reference with accession and version
    (
        'NC_000001.10', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '10',
            }
        }
    ),
    # - lrg reference
    (
        'LRG_1', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_1',
            }
        }
    ),
    # - lrg reference with version - should not be possible
    (
        'LRG_1.1', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_1',
                'version': '1',
            },
        }
    ),
    # Specific locus present
    # - with gene names only
    (
        'NC_000001(SDHD)', {
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
        'NC_012920.1(MT-TL1)', {
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
        'NG_012337.1(TIMM8B)', {
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
        'NC_000001(SDHD_v001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
                'transcript_variant': '001',
            }
        }
    ),
    (
        'NC_000001(SDHD_i001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
                'protein_isoform': '001',
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_v001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'TIMM8B',
                'transcript_variant': '001'
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_i001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'TIMM8B',
                'protein_isoform': '001'
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_v001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_012920',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1',
                'transcript_variant': '001',
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_i001)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_012920',
                'version': '1',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'MT-TL1',
                'protein_isoform': '001',
            }
        }
    ),
    # - with accession and version
    (
        'NG_012337.1(NM_012459.2)', {
            'reference': {
                'type': 'genbank',
                'accession': 'NG_012337',
                'version': '1',
            },
            'specific_locus': {
                'type': 'genbank',
                'accession': 'NM_012459',
                'version': '2',
            }
        }
    ),
    # - LRG ones
    (
        'LRG_24t1', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_24',
            },
            'specific_locus': {
                'type': 'lrg transcript',
                'transcript_variant': 't1',
            }
        }
    ),
    (
        'LRG_24p1', {
            'reference': {
                'type': 'lrg',
                'id': 'LRG_24',
            },
            'specific_locus': {
                'type': 'lrg protein',
                'protein_isoform': 'p1',
            }
        }
    ),
    # - mix
    (
        'NC_000001.1t1', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '1',
            },
            'specific_locus': {
                'type': 'lrg transcript',
                'transcript_variant': 't1',
            },
        }
    ),
    (
        'NC_000001.1p1', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '1',
            },
            'specific_locus': {
                'type': 'lrg protein',
                'protein_isoform': 'p1',
            },
        }
    ),
    (
        'LRG_24(SDHD)', {
            'reference': {
                'id': 'LRG_24',
                'type': 'lrg'
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
            },
        }
    ),
]


@pytest.mark.parametrize('description,model', REFERENCES)
def test_reference_part(description, model):
    """
    Test the reference part of a description.
    """
    parser = HgvsParser(start_rule='reference')

    assert parse_tree_to_model(parser.parse(description)) == model


VARIANTS = [
    # Substitutions
    (
        '100C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'location': {
                        'type': 'point',
                        'position': 100
                    },
                    'insertions': [
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
                        'type': 'point',
                        'position': 100,
                        'offset': 3
                    },
                    'insertions': [
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
                        'type': 'point',
                        'position': 100,
                        'outside_cds': 'downstream'
                    },
                    'insertions': [
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
                        'type': 'point',
                        'position': 1,
                        'offset': -3,
                        'outside_cds': 'downstream'
                    },
                    'insertions': [
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
                        'type': 'point',
                        'position': 1,
                        'offset': 3,
                        'outside_cds': 'upstream'
                    },
                    'insertions': [
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
                        'type': 'point',
                        'position': 10
                    }
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
                        'type': 'point',
                        'position': 10
                    },
                    'deleted': [
                        {
                            'sequence': 'A',
                            'source': 'description'
                        }
                    ]
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
                        'type': 'point',
                        'position': 100,
                        'offset': 1
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10,
                            'offset': -1
                        },
                        'end': {
                            'type': 'point',
                            'position': 20,
                            'offset': -3
                        }
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 15
                        }
                    },
                    'deleted': [
                        {
                            'source': 'description',
                            'length': 5
                        }
                    ]
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
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'start': {
                                'type': 'point',
                                'position': 10
                            },
                            'end': {
                                'type': 'point',
                                'position': 20
                            },
                            'uncertain': True
                        },
                        'end': {
                            'type': 'point',
                            'position': 30
                        }
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'start': {
                                'type': 'point',
                                'position': 10
                            },
                            'end': {
                                'type': 'point',
                                'position': 20
                            },
                            'uncertain': True
                        },
                        'end': {
                            'type': 'range',
                            'start': {
                                'type': 'point',
                                'position': 30
                            },
                            'end': {
                                'type': 'point',
                                'position': 40
                            },
                            'uncertain': True
                        }
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'start': {
                                'type': 'point',
                                'uncertain': True
                            },
                            'end': {
                                'type': 'point',
                                'position': 20,
                                'outside_cds': 'upstream'
                            },
                            'uncertain': True
                        },
                        'end': {
                            'type': 'range',
                            'start': {
                                'type': 'point',
                                'position': 30,
                                'offset': 1
                            },
                            'end': {
                                'type': 'point',
                                'position': 30,
                                'offset': -1
                            },
                            'uncertain': True
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
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'uncertain': True
                            },
                            'end': {
                                'type': 'point',
                                'position': 1,
                                'outside_cds': 'upstream'
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 1,
                                'outside_cds': 'downstream'
                            },
                            'end': {
                                'type': 'point',
                                'uncertain': True
                            }
                        }
                    }
                }
            ]
        }
    ),
    (
        '(?_-1+?)_(*1-?_?)del',
        {
            'variants': [
                {
                    'type': 'del',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'uncertain': True
                            },
                            'end': {
                                'type': 'point',
                                'position': 1,
                                'outside_cds': 'upstream',
                                'uncertain_offset': '+?'
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 1,
                                'outside_cds': 'downstream',
                                'uncertain_offset': '-?'
                            },
                            'end': {
                                'type': 'point',
                                'uncertain': True
                            }
                        }
                    }
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
                        'type': 'point',
                        'position': 10
                    },
                }
            ]
        }
    ),
    # Insertions
    (
        '11_12insT',
        {
            'variants': [
                {
                    'type': 'ins',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'location': {
                                'type': 'range',
                                'start': {
                                    'type': 'point',
                                    'position': 10
                                },
                                'end': {
                                    'type': 'point',
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'location': {
                                'type': 'range',
                                'start': {
                                    'type': 'point',
                                    'position': 10
                                },
                                'end': {
                                    'type': 'point',
                                    'position': 20
                                }
                            },
                            'inverted': True
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'location': {
                                'type': 'range',
                                'start': {
                                    'type': 'point',
                                    'position': 10
                                },
                                'end': {
                                    'type': 'point',
                                    'position': 20
                                }
                            },
                            'inverted': True
                        },
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1',
                                    'type': 'genbank'
                                },
                                'coordinate_system': 'c',
                                'location': {
                                    'type': 'range',
                                    'start': {
                                        'type': 'point',
                                        'position': 100
                                    },
                                    'end': {
                                        'type': 'point',
                                        'position': 200
                                    }
                                }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1',
                                    'type': 'genbank'
                                },
                                'coordinate_system': 'c',
                                'location': {
                                    'type': 'range',
                                    'start': {
                                        'type': 'point',
                                        'position': 100
                                    },
                                    'end': {
                                        'type': 'point',
                                        'position': 200
                                    }
                                }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1',
                                    'type': 'genbank'
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    }
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    },
                    'insertions': [
                        {
                            'location': {
                                'type': 'range',
                                'start': {
                                    'type': 'point',
                                    'position': 30
                                },
                                'end': {
                                    'type': 'point',
                                    'position': 40
                                }
                            }
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
                        'type': 'point',
                        'position': 10
                    },
                    'insertions': [
                        {
                            'sequence': 'GA',
                            'source': 'description'
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'GA',
                            'source': 'description'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '10_20del10insGA',
        {
            'variants': [
                {
                    'type': 'delins',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    },
                    'deleted': [
                        {
                            'length': 10,
                            'source': 'description'
                        }
                    ],
                    'insertions': [
                        {
                            'sequence': 'GA',
                            'source': 'description'
                        }
                    ]
                }
            ]
        }
    ),
    (
        '10delAinsGA',
        {
            'variants': [
                {
                    'type': 'delins',
                    'location': {
                        'type': 'point',
                        'position': 10
                    },
                    'deleted': [
                        {
                            'sequence': 'A',
                            'source': 'description'
                        }
                    ],
                    'insertions': [
                        {
                            'sequence': 'GA',
                            'source': 'description'
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
                        'type': 'point',
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
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    }
                }
            ]
        }
    ),
    # Multiple variants (allele)
    (
        '[10=;11_12ins[T;10_20inv;NM_000001.1:c.100_200];10_20delinsGA]',
        {
            'variants': [
                {
                    'type': 'equal',
                    'location': {
                        'type': 'point',
                        'position': 10
                    }
                },
                {
                    'type': 'ins',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 11
                        },
                        'end': {
                            'type': 'point',
                            'position': 12
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'location': {
                                'type': 'range',
                                'start': {
                                    'type': 'point',
                                    'position': 10
                                },
                                'end': {
                                    'type': 'point',
                                    'position': 20
                                }
                            },
                            'inverted': True
                        },
                        {
                            'reference_location': {
                                'reference': {
                                    'accession': 'NM_000001',
                                    'version': '1',
                                    'type': 'genbank'
                                },
                                'coordinate_system': 'c',
                                'location': {
                                    'type': 'range',
                                    'start': {
                                        'type': 'point',
                                        'position': 100
                                    },
                                    'end': {
                                        'type': 'point',
                                        'position': 200
                                    }
                                }
                            }
                        }
                    ]
                },
                {
                    'type': 'delins',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 20
                        }
                    },
                    'insertions': [
                        {
                            'sequence': 'GA',
                            'source': 'description'
                        }
                    ]
                }
            ]
        }
    )
]


@pytest.mark.parametrize('description,model', VARIANTS)
def test_variants(description, model):
    """
    Test the variants part of a description.
    """
    parser = HgvsParser(start_rule='variants')

    assert parse_tree_to_model(parser.parse(description)) == model
