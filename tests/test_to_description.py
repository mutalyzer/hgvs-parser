"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.to_description import model_to_description


MODELS = [
    (
        'NC_000001:10_20=', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
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
    (
        'NC_000001.10:c.(?_-1)_(*1_?)del', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
                'version': '10',
            },
            'coordinate_system': 'c',
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
        'NC_000001(SDHD_v001):g.-1+3C>A', {
            'reference': {
                'type': 'genbank',
                'accession': 'NC_000001',
            },
            'specific_locus': {
                'type': 'gene',
                'id': 'SDHD',
                'transcript_variant': '001',
            },
            'coordinate_system': 'g',
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
    )
]


@pytest.mark.parametrize('description,model', MODELS)
def test_model_to_description(description, model):
    assert model_to_description(model) == description

