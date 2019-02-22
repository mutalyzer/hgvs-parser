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
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                }
            }
        }
    ),
    # - genbank reference with accession and version
    (
        'NC_000001.10', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'version': '10',
                }
            }
        }
    ),
    # - genbank reference with accession, version and coordinate system
    (
        'NC_000001.10:c.', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'version': '10',
                    'coordinate_system': 'c',
                }
            }
        }
    ),
    # - lrg reference
    (
        'LRG_1', {
            'references': {
                'reference': {
                    'type': 'lrg',
                    'id': 'LRG_1',
                }
            }
        }
    ),
    # - lrg reference with coordinate system
    (
        'LRG_1:g.', {
            'references': {
                'reference': {
                    'type': 'lrg',
                    'id': 'LRG_1',
                    'coordinate_system': 'g'
                }
            }
        }
    ),
    # - lrg reference with version - the user should be notified somehow
    (
        'LRG_1.1', {
            'references': {
                'reference': {
                    'type': 'lrg',
                    'id': 'LRG_1',
                    'version': '1',
                }
            }
        }
    ),
    # Specific locus present
    # - with gene names only
    (
        'NC_000001(SDHD)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'SDHD',
                    }
                }
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_012920',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'MT-TL1',
                    }
                }
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NG_012337',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'TIMM8B',
                    }
                }
            }
        }
    ),
    (
        'NC_000001(SDHD_v001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'SDHD',
                        'transcript_variant': '001',
                    }
                }
            }
        }
    ),
    (
        'NC_000001(SDHD_i001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'SDHD',
                        'protein_isoform': '001',
                    }
                }
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_v001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NG_012337',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'TIMM8B',
                        'transcript_variant': '001'
                    }
                }
            }
        }
    ),
    (
        'NG_012337.1(TIMM8B_i001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NG_012337',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'TIMM8B',
                        'protein_isoform': '001'
                    }
                }
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_v001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_012920',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'MT-TL1',
                        'transcript_variant': '001',
                    }
                }
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_i001)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_012920',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'MT-TL1',
                        'protein_isoform': '001',
                    }
                }
            }
        }
    ),
    (
        'NC_012920.1(MT-TL1_i001):c.', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_012920',
                    'version': '1',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'MT-TL1',
                        'protein_isoform': '001',
                    },
                    'coordinate_system': 'c'
                }
            }
        }
    ),
    # - with accession and version
    (
        'NG_012337.1(NM_012459.2)', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NG_012337',
                    'version': '1',
                    'specific_locus': {
                        'type': 'genbank',
                        'accession': 'NM_012459',
                        'version': '2',
                    }
                }
            }
        }
    ),
    # - LRG ones
    (
        'LRG_24t1', {
            'references': {
                'reference': {
                    'type': 'lrg',
                    'id': 'LRG_24',
                    'specific_locus': {
                        'type': 'lrg transcript',
                        'transcript_variant': 't1',
                    }
                }
            }
        }
    ),
    (
        'LRG_24p1', {
            'references': {
                'reference': {
                    'type': 'lrg',
                    'id': 'LRG_24',
                    'specific_locus': {
                        'type': 'lrg protein',
                        'protein_isoform': 'p1',
                    }
                }
            }
        }
    ),
    # - mix
    (
        'NC_000001.1t1', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'version': '1',
                    'specific_locus': {
                        'type': 'lrg transcript',
                        'transcript_variant': 't1',
                    }
                }
            }
        }
    ),
    (
        'NC_000001.1p1', {
            'references': {
                'reference': {
                    'type': 'genbank',
                    'accession': 'NC_000001',
                    'version': '1',
                    'specific_locus': {
                        'type': 'lrg protein',
                        'protein_isoform': 'p1',
                    }
                }
            }
        }
    ),
    (
        'LRG_24(SDHD)', {
            'references': {
                'reference': {
                    'id': 'LRG_24',
                    'type': 'lrg',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'SDHD',
                    }
                }
            }
        }
    ),
    (
        'LRG_24(SDHD):c.', {
            'references': {
                'reference': {
                    'id': 'LRG_24',
                    'type': 'lrg',
                    'specific_locus': {
                        'type': 'gene',
                        'id': 'SDHD',
                    },
                    'coordinate_system': 'c'
                }
            }
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
        '101C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
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
        '101+3C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 100,
                        'offset': {
                            'value': 3
                        }
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
        '*101C>A',
        {
            'variants': [
                {
                    'type': 'substitution',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 100,
                        'outside_cds': 'downstream'
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
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 0,
                        'offset': {
                            'value': -3,
                        },
                        'outside_cds': 'downstream'
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
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 0,
                        'offset': {
                            'value': 3,
                        },
                        'outside_cds': 'upstream'
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
        '11del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
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
        '11delA',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
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
        '101+1del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 100,
                        'offset': {
                            'value': 1
                        }
                    }
                }
            ]
        }
    ),
    (
        '11_21del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
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
        '11-1_21-3del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10,
                            'offset': {
                                'value': -1
                            }
                        },
                        'end': {
                            'type': 'point',
                            'position': 20,
                            'offset': {
                                'value': -3
                            }
                        }
                    }
                }
            ]
        }
    ),
    (
        # Note: the addition of '5' is not HGVS.
        '11_16del5',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
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
        '(11_16)del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'uncertain': True,
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 15
                        },
                    }
                }
            ]
        }
    ),
    (
        '(11_21)_31del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 10
                            },
                            'end': {
                                'type': 'point',
                                'position': 20
                            }
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
        '(11_21)_(31_41)del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 10
                            },
                            'end': {
                                'type': 'point',
                                'position': 20
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
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
                }
            ]
        }
    ),
    (
        '(?_-21)_(31+1_31-1)del',
        {
            'variants': [
                {
                    'type': 'deletion',
                    'source': 'reference',
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
                                'position': 20,
                                'outside_cds': 'upstream'
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 30,
                                'offset': {
                                    'value': 1
                                }
                            },
                            'end': {
                                'type': 'point',
                                'position': 30,
                                'offset': {
                                    'value': -1
                                }
                            }
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
                    'type': 'deletion',
                    'source': 'reference',
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
                                'position': 0,
                                'outside_cds': 'upstream'
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 0,
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
                    'type': 'deletion',
                    'source': 'reference',
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
                                'position': 0,
                                'outside_cds': 'upstream',
                                'offset': {
                                    'uncertain': True
                                }
                            }
                        },
                        'end': {
                            'type': 'range',
                            'uncertain': True,
                            'start': {
                                'type': 'point',
                                'position': 0,
                                'outside_cds': 'downstream',
                                'offset':  {
                                    'uncertain': True
                                }
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
        '11dup',
        {
            'variants': [
                {
                    'type': 'duplication',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 10
                    },
                }
            ]
        }
    ),
    # Insertions
    #  - note that one of the reasons why 'source' is present also at the
    #    variant level (and not only in the 'inserted') is that an 'insertion'
    #    is considered a special case of a 'deletion_insertion'.
    (
        '11_12insT',
        {
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
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
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
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
        '11_12ins[T;11_21]',
        {
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [{
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'source': 'reference',
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
        '11_12ins[T;11_21inv]',
        {
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'source': 'reference',
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
        '11_12ins[T;11_21inv;NM_000001.1:c.101_201]',
        {
            'references': {
                'NM_000001.1': {
                    'accession': 'NM_000001',
                    'version': '1',
                    'type': 'genbank'
                },
            },
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'source': 'reference',
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
                            'source': 'NM_000001.1:c.',
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
                    ]
                }
            ]
        }
    ),
    (
        '11_12insNM_000001.1:c.101_201',
        {
            'references': {
                'NM_000001.1': {
                    'accession': 'NM_000001',
                    'version': '1',
                    'type': 'genbank'
                },
            },
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'source': 'NM_000001.1:c.',
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
                    ]
                }
            ]
        }
    ),
    (
        '11_12insNM_000001.1',
        {
            'references': {
                'NM_000001.1': {
                    'accession': 'NM_000001',
                    'version': '1',
                    'type': 'genbank'
                },
            },
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'source': 'NM_000001.1',
                        }
                    ]
                }
            ]
        }
    ),
    (
        '11_12insNG_000001.1(NM_000002.3):c.100',
        {
            'references': {
                'NG_000001.1': {
                    'accession': 'NG_000001',
                    'version': '1',
                    'type': 'genbank'
                },
            },
            'variants': [
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'source': 'NG_000001.1(NM_000002.3):c.',
                            'location': {
                                'type': 'point',
                                'position': 99
                            },
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
                    'type': 'inversion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    }
                }
            ]
        }
    ),
    # Conversions
    (
        '11_21con31_41',
        {
            'variants': [
                {
                    'type': 'conversion',
                    'source': 'reference',
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
                    'inserted': [
                        {
                            'source': 'reference',
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
    # Deletion-inserted
    (
        '11delinsGA',
        {
            'variants': [
                {
                    'type': 'deletion_insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 10
                    },
                    'inserted': [
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
        '11_21delinsGA',
        {
            'variants': [
                {
                    'type': 'deletion_insertion',
                    'source': 'reference',
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
                    'inserted': [
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
        '11_21del10insGA',
        {
            'variants': [
                {
                    'type': 'deletion_insertion',
                    'source': 'reference',
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
                    'inserted': [
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
        '11delAinsGA',
        {
            'variants': [
                {
                    'type': 'deletion_insertion',
                    'source': 'reference',
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
                    'inserted': [
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
    #                 'inserted': [
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
    #                 'inserted': [
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
        '=',
        {
            'variants': [
                {
                    'type': 'equal',
                    'source': 'reference',
                }
            ]
        }
    ),
    (
        '11=',
        {
            'variants': [
                {
                    'type': 'equal',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 10
                    }
                }
            ]
        }
    ),
    (
        '11_21=',
        {
            'variants': [
                {
                    'type': 'equal',
                    'source': 'reference',
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
        '[11=;11_12ins[T;11_21inv;NM_000001.1:c.101_201];11_21delinsGA]',
        {
            'references': {
                'NM_000001.1': {
                    'accession': 'NM_000001',
                    'version': '1',
                    'type': 'genbank'
                },
            },
            'variants': [
                {
                    'type': 'equal',
                    'source': 'reference',
                    'location': {
                        'type': 'point',
                        'position': 10
                    }
                },
                {
                    'type': 'insertion',
                    'source': 'reference',
                    'location': {
                        'type': 'range',
                        'start': {
                            'type': 'point',
                            'position': 10
                        },
                        'end': {
                            'type': 'point',
                            'position': 11
                        }
                    },
                    'inserted': [
                        {
                            'sequence': 'T',
                            'source': 'description'
                        },
                        {
                            'source': 'reference',
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
                            'source': 'NM_000001.1:c.',
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
                    ]
                },
                {
                    'type': 'deletion_insertion',
                    'source': 'reference',
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
                    'inserted': [
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
