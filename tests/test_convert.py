"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from mutalyzer_hgvs_parser.hgvs_parser import HgvsParser
from mutalyzer_hgvs_parser.convert import description_to_model, _location_to_model, \
    _variant_to_model, _variants_to_model, _inserted_to_model,\
    _reference_to_model


def get_tests(tests):
    return [(k, tests[k]) for k in tests.keys()]


REFERENCES = {
    'R1': {'id': 'R1'},
    'R1(R2)': {'id': 'R1',
               'selector': {'id': 'R2'}},
    'R1(R2(R3))': {'id': 'R1',
                   'selector': {'id': 'R2',
                                'selector': {'id': 'R3'}}},
    'NM_000001.1': {'id': 'NM_000001.1'},
    'NG_000001.1(NM_000002.3)': {'id': 'NG_000001.1',
                                 'selector': {'id': 'NM_000002.3'}}
}


@pytest.mark.parametrize('reference, model', get_tests(REFERENCES))
def test_reference_to_model(reference, model):
    parser = HgvsParser(start_rule='reference')
    assert _reference_to_model(parser.parse(reference)) == model


LOCATIONS = {
    '1': {'type': 'point',
          'position': 1},
    '10': {'type': 'point',
           'position': 10},
    '100': {'type': 'point',
            'position': 100},
    '10-20': {'type': 'point',
              'position': 10,
              'offset': {'value': -20}},
    '10+20': {'type': 'point',
              'position': 10,
              'offset': {'value': +20}},
    '?': {'type': 'point',
          'uncertain': True},
    '??': {'type': 'point',
           'uncertain': True,
           'offset': {'uncertain': True}},
    '?+?': {'type': 'point',
            'uncertain': True,
            'offset': {'uncertain': True,
                       'downstream': True}},
    '?-?': {'type': 'point',
            'uncertain': True,
            'offset': {'uncertain': True,
                       'upstream': True}},
    '-10': {'type': 'point',
            'position': 10,
            'outside_cds': 'upstream'},
    '-10-20': {'type': 'point',
               'position': 10,
               'outside_cds': 'upstream',
               'offset': {'value': -20}},
    '-10+20': {'type': 'point',
               'position': 10,
               'outside_cds': 'upstream',
               'offset': {'value': 20}},
    '*10': {'type': 'point',
            'position': 10,
            'outside_cds': 'downstream'},
    '*10+20': {'type': 'point',
               'position': 10,
               'outside_cds': 'downstream',
               'offset': {'value': 20}},
    '*10-20': {'type': 'point',
               'position': 10,
               'outside_cds': 'downstream',
               'offset': {'value': -20}},
    '10_15': {'type': 'range',
              'start': {'type': 'point',
                        'position': 10},
              'end': {'type': 'point',
                      'position': 15}},
    '(10_15)': {'type': 'range',
                'uncertain': True,
                'start': {'type': 'point',
                          'position': 10},
                'end': {'type': 'point',
                        'position': 15}},
    '(10_20)_30': {'type': 'range',
                   'start': {'type': 'range',
                             'uncertain': True,
                             'start': {'type': 'point',
                                       'position': 10},
                             'end': {'type': 'point',
                                     'position': 20}},
                   'end': {'type': 'point',
                           'position': 30}},
    '10_(20_30)': {'type': 'range',
                   'start': {'type': 'point',
                             'position': 10},
                   'end': {'type': 'range',
                           'uncertain': True,
                           'start': {'type': 'point',
                                     'position': 20},
                           'end': {'type': 'point',
                                   'position': 30}}},
    '(10_20)_(30_40)': {'type': 'range',
                        'start': {'type': 'range',
                                  'uncertain': True,
                                  'start': {'type': 'point',
                                            'position': 10},
                                  'end': {'type': 'point',
                                          'position': 20}},
                        'end': {'type': 'range',
                                'uncertain': True,
                                'start': {'type': 'point',
                                          'position': 30},
                                'end': {'type': 'point',
                                        'position': 40}}},
    '(?_-20)_(30+1_30-1)': {'type': 'range',
                            'start': {'type': 'range',
                                      'uncertain': True,
                                      'start': {'type': 'point',
                                                'uncertain': True},
                                      'end': {'type': 'point',
                                              'position': 20,
                                              'outside_cds': 'upstream'}},
                            'end': {'type': 'range',
                                    'uncertain': True,
                                    'start': {'type': 'point',
                                              'position': 30,
                                              'offset': {'value': 1}},
                                    'end': {'type': 'point',
                                            'position': 30,
                                            'offset': {'value': -1}}}},
    '(?_-1)_(*1_?)': {'type': 'range',
                      'start': {'type': 'range',
                                'uncertain': True,
                                'start': {'type': 'point',
                                          'uncertain': True},
                                'end': {'type': 'point',
                                        'position': 1,
                                        'outside_cds': 'upstream'}},
                      'end': {'type': 'range',
                              'uncertain': True,
                              'start': {'type': 'point',
                                        'position': 1,
                                        'outside_cds': 'downstream'},
                              'end': {'type': 'point',
                                      'uncertain': True}}},
    '(?_-1+?)_(*1-?_?)': {'type': 'range',
                          'start': {'type': 'range',
                                    'uncertain': True,
                                    'start': {'type': 'point',
                                              'uncertain': True},
                                    'end': {'type': 'point',
                                            'position': 1,
                                            'outside_cds': 'upstream',
                                            'offset': {'uncertain': True,
                                                       'downstream': True}}},
                          'end': {'type': 'range',
                                  'uncertain': True,
                                  'start': {'type': 'point',
                                            'position': 1,
                                            'outside_cds': 'downstream',
                                            'offset': {'uncertain': True,
                                                       'upstream': True}},
                                  'end': {'type': 'point',
                                          'uncertain': True}}},
    '10_11': {'type': 'range',
              'start': {'type': 'point',
                        'position': 10},
              'end': {'type': 'point',
                      'position': 11}},
    '10_20': {'type': 'range',
              'start': {'type': 'point',
                        'position': 10},
              'end': {'type': 'point',
                      'position': 20}},
    '40_50': {'type': 'range',
              'start': {'type': 'point',
                        'position': 40},
              'end': {'type': 'point',
                      'position': 50}},
    '200_300': {'type': 'range',
                'start': {'type': 'point',
                          'position': 200},
                'end': {'type': 'point',
                        'position': 300}},
    '123_191': {'type': 'range',
                'start': {'type': 'point',
                          'position': 123},
                'end': {'type': 'point',
                        'position': 191}},
}


LENGTHS = {
    '4': {'value': 4,
          'type': 'point'},
    '6': {'value': 6,
          'type': 'point'},
    '10': {'value': 10,
           'type': 'point'},
    '19': {'value': 19,
           'type': 'point'},
    '20': {'type': 'point',
           'value': 20},
    '(10)': {'value': 10,
             'type': 'point'},
    '(10_20)': {'type': 'range',
                'uncertain': True,
                'start': {'type': 'point',
                          'value': 10},
                'end': {'type': 'point',
                        'value': 20}},
    '(?_20)': {'type': 'range',
               'uncertain': True,
               'start': {'type': 'point',
                         'uncertain': True},
               'end': {'type': 'point',
                       'value': 20}},
}


@pytest.mark.parametrize('description, model', get_tests(LOCATIONS))
def test_location_to_model(description, model):
    parser = HgvsParser(start_rule='location')
    assert _location_to_model(parser.parse(description)) == model


INSERTED = {
    'A': [{'sequence': 'A',
           'source': 'description'}],
    'GA': [{'sequence': 'GA',
            'source': 'description'}],
    '10': [{'length': LENGTHS['10']}],
    '(10)': [{'length': LENGTHS['(10)']}],
    '(10_20)': [{'length': LENGTHS['(10_20)']}],
    '(?_20)': [{'length': LENGTHS['(?_20)']}],
    '10_20': [{'source': 'reference',
               'location': LOCATIONS['10_20']}],
    '[A;10_20]': [{'sequence': 'A',
                   'source': 'description'},
                  {'source': 'reference',
                   'location': LOCATIONS['10_20']}],
    '[A;10_20inv]': [{'sequence': 'A',
                      'source': 'description'},
                     {'source': 'reference',
                      'location': LOCATIONS['10_20'],
                      'inverted': True}],
    'R2:g.10_15': [{'source': {'id': 'R2'},
                    'coordinate_system': 'g',
                    'location': LOCATIONS['10_15']}],
    'NG_000001.1(NM_000002.3):c.100': [{'source':
                                            REFERENCES[
                                                'NG_000001.1(NM_000002.3)'],
                                        'coordinate_system': 'c',
                                        'location': LOCATIONS['100']}],
    '[R2:g.200_300;40_50]': [{'source': {'id': 'R2'},
                              'coordinate_system': 'g',
                              'location': LOCATIONS['200_300']},
                             {'source': 'reference',
                              'location': LOCATIONS['40_50']}],
    '[T;10_20inv;NM_000001.1:c.200_300]': [{'sequence': 'T',
                                            'source': 'description'},
                                           {'source': 'reference',
                                            'location': LOCATIONS['10_20'],
                                            'inverted': True},
                                           {'source': {'id': 'NM_000001.1'},
                                            'coordinate_system': 'c',
                                            'location': LOCATIONS['200_300']}]
}

DELETED = {}


@pytest.mark.parametrize('description, model', get_tests(INSERTED))
def test_inserted_to_model(description, model):
    parser = HgvsParser(start_rule='inserted')
    assert _inserted_to_model(parser.parse(description)) == model


VARIANTS = {
    '1': {'location': LOCATIONS['1']},
    '10_15': {'location': LOCATIONS['10_15']},
    # Substitutions
    '10C>A': {'type': 'substitution',
              'source': 'reference',
              'location': LOCATIONS['10'],
              'deleted': [{'sequence': 'C',
                           'source': 'description'}],
              'inserted': [{'sequence': 'A',
                            'source': 'description'}]},
    '10>A': {'type': 'substitution',
             'source': 'reference',
             'location': LOCATIONS['10'],
             'inserted': INSERTED['A']},
    '10>R2:g.10_15': {'type': 'substitution',
                      'source': 'reference',
                      'location': LOCATIONS['10'],
                      'inserted': INSERTED['R2:g.10_15']},
    '10>[R2:g.200_300;40_50]': {'type': 'substitution',
                                'source': 'reference',
                                'location': LOCATIONS['10'],
                                'inserted': INSERTED['[R2:g.200_300;40_50]']},
    # Deletions
    '10del': {'type': 'deletion',
              'source': 'reference',
              'location': LOCATIONS['10']},
    '10delA': {'type': 'deletion',
               'source': 'reference',
               'location': LOCATIONS['10'],
               'deleted': [{'sequence': 'A',
                            'source': 'description'}]},
    '10_15del6': {'type': 'deletion',
                  'source': 'reference',
                  'location': LOCATIONS['10_15'],
                  'deleted': [{'length': {'value': 6,
                                          'type': 'point'}}]},
    # Duplications
    '10dup': {'type': 'duplication',
              'source': 'reference',
              'location': LOCATIONS['10']},
    # Insertions
    '10_11insA': {'type': 'insertion',
                  'source': 'reference',
                  'location': LOCATIONS['10_11'],
                  'inserted': INSERTED['A']},
    '10_11ins[A]': {'type': 'insertion',
                    'source': 'reference',
                    'location': LOCATIONS['10_11'],
                    'inserted': INSERTED['A']},
    '10_11ins[A;10_20]': {'type': 'insertion',
                          'source': 'reference',
                          'location': LOCATIONS['10_11'],
                          'inserted': INSERTED['[A;10_20]']},
    '10_11ins[A;10_20inv]': {'type': 'insertion',
                             'source': 'reference',
                             'location': LOCATIONS['10_11'],
                             'inserted': INSERTED['[A;10_20inv]']},
    '10_11ins[T;10_20inv;NM_000001.1:c.200_300]': {
        'type': 'insertion',
        'source': 'reference',
        'location': LOCATIONS['10_11'],
        'inserted': INSERTED['[T;10_20inv;NM_000001.1:c.200_300]']},
    '10_11insNM_000001.1:c.100_200': {
        'type': 'insertion',
        'source': 'reference',
        'location': LOCATIONS['10_11'],
        'inserted': [{'source': {'id': 'NM_000001.1'},
                      'coordinate_system': 'c',
                      'location': {'type': 'range',
                                   'start': {'type': 'point',
                                             'position': 100},
                                   'end': {'type': 'point',
                                           'position': 200}}}]},
    # TODO: Check if just a reference should be considered a description.
    # '10_11insNM_000001.1': {'type': 'insertion',
    #                         'source': 'reference',
    #                         'location': LOCATIONS['10_11'],
    #                         'inserted': [{'source': {'id': 'NM_000001.1'}}]},
    '10_11insNG_000001.1(NM_000002.3):c.100': {
        'type': 'insertion',
        'source': 'reference',
        'location': LOCATIONS['10_11'],
        'inserted': [{'source': {'id': 'NG_000001.1',
                                 'selector': {'id': 'NM_000002.3'}},
                      'coordinate_system': 'c',
                      'location': {'type': 'point',
                                   'position': 100}}]},
    # Inversions
    '10_11inv': {'type': 'inversion',
                 'source': 'reference',
                 'location': LOCATIONS['10_11']},
    # Conversions
    '10_20con40_50': {'type': 'conversion',
                      'source': 'reference',
                      'location': LOCATIONS['10_20'],
                      'inserted': [{'source': 'reference',
                                    'location': LOCATIONS['40_50']}]},
    # Deletion insertions
    '10delinsGA': {'type': 'deletion_insertion',
                   'source': 'reference',
                   'location': LOCATIONS['10'],
                   'inserted': INSERTED['GA']},
    '10_20delinsGA': {'type': 'deletion_insertion',
                      'source': 'reference',
                      'location': LOCATIONS['10_20'],
                      'inserted': INSERTED['GA']},
    '10_20del10insGA': {'type': 'deletion_insertion',
                        'source': 'reference',
                        'location': LOCATIONS['10_20'],
                        'deleted': [{'length': {'value': 10,
                                                'type': 'point'}}],
                        'inserted': INSERTED['GA']},
    '10delAinsGA': {'type': 'deletion_insertion',
                    'source': 'reference',
                    'location': LOCATIONS['10'],
                    'deleted': [{'sequence': 'A',
                                 'source': 'description'}],
                    'inserted': INSERTED['GA']},
    '10_11delinsR2:g.10_15': {'type': 'deletion_insertion',
                              'source': 'reference',
                              'location': LOCATIONS['10_11'],
                              'inserted': INSERTED['R2:g.10_15']},
    # Repeats
    '10GA[20]': {'type': 'repeat',
                 'source': 'reference',
                 'location': LOCATIONS['10'],
                 'inserted': [{'sequence': 'GA',
                               'length': LENGTHS['20']}]},
    '123_191CAG[19]CAA[4]': {'type': 'repeat',
                             'source': 'reference',
                             'location':  LOCATIONS['123_191'],
                             'inserted': [{'sequence': 'CAG',
                                           'length': LENGTHS['19']},
                                          {'sequence': 'CAA',
                                           'length': LENGTHS['4']}]},
    # No changes (equal)
    # '=': [],
    '10=': {'type': 'equal'
        ,'source': 'reference',
            'location': LOCATIONS['10']},
    '10_20=': {'type': 'equal',
               'source': 'reference',
               'location': LOCATIONS['10_20']},
    '10del20': {'type': 'deletion',
                'source': 'reference',
                'location': LOCATIONS['10'],
                'deleted': [{'length': LENGTHS['20']}]},
    '10del10_20': {'type': 'deletion',
                   'source': 'reference',
                   'location': LOCATIONS['10'],
                   'deleted': [{'source': 'reference',
                                'location': LOCATIONS['10_20']}]}
}


@pytest.mark.parametrize('variant, model', get_tests(VARIANTS))
def test_variants_to_model(variant, model):
    parser = HgvsParser(start_rule='variant')
    assert _variant_to_model(parser.parse(variant)) == model


DESCRIPTIONS = {
    'R1(R2(R3)):g.[10del;10_11delinsR2:g.10_15]': {
        'reference': REFERENCES['R1(R2(R3))'],
        'coordinate_system': 'g',
        'variants': [VARIANTS['10del'],
                     VARIANTS['10_11delinsR2:g.10_15']]},
    'R1:g.[10=;10_11ins[T;10_20inv;NM_000001.1:c.200_300];10_20delinsGA]': {
        'reference': REFERENCES['R1'],
        'coordinate_system': 'g',
        'variants': [VARIANTS['10='],
                     VARIANTS['10_11ins[T;10_20inv;NM_000001.1:c.200_300]'],
                     VARIANTS['10_20delinsGA']]},
}


@pytest.mark.parametrize('description, model', get_tests(DESCRIPTIONS))
def test_convert(description, model):
    parser = HgvsParser()
    assert description_to_model(parser.parse(description)) == model


OPERATIONS_MIX = {
    '>': 'substitution',
    'ins': 'insertion',
    'delins': 'deletion_insertion'
}


def compose_description_model(reference, location, operation, insert):
    description = '{}:{}{}{}'.format(reference, location, operation, insert)
    model = {
        'reference': REFERENCES[reference],
        'variants': [{
            'type': OPERATIONS_MIX[operation],
            'source': 'reference',
            'location': LOCATIONS[location],
            'inserted': INSERTED[insert],
        }]
    }
    return {description: model}


def get_mix():
    descriptions = {}
    for operation in OPERATIONS_MIX:
        for reference in REFERENCES:
            for location in LOCATIONS:
                for insert in INSERTED:
                    descriptions.update(compose_description_model(
                        reference, location, operation, insert))
    return descriptions


@pytest.mark.parametrize('description, model', get_tests(get_mix()))
def test_mix(description, model):
    parser = HgvsParser()
    assert description_to_model(parser.parse(description)) == model
