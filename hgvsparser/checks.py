"""
Model checks.
"""
import json


def check(model):
    info = {
        'errors': [],
        'warnings': [],
        'extras': []
    }
    basic_checks(model, info)

    reference_check(model.get('reference'), info)

    specific_locus_check(model.get('reference'), model.get('specific_locus'),
                         info)

    variants_check(model, info)

    print('\nModel check summary:')
    print(json.dumps(info, indent=2))


def basic_checks(model, info):
    if not isinstance(model, dict):
        info['errors'].append('The model not a dictionary.')
        return
    if model.get('reference') is None:
        info['errors'].append('Reference not found.')
    if model.get('variants') is None:
        info['errors'].append('Variants not found.')


def reference_check(reference, info):
    if not isinstance(reference, dict):
        info['errors'].append('The reference is not a dictionary.')
        return
    if reference.get('type') is None:
        info['errors'].append('Reference type not found.')
    if reference['type'] == 'genbank':
        if reference.get('accession') and (reference.get('version') is None):
            info['warnings'] = 'No version specified. The most recent found ' \
                               'version will be considered.'


def specific_locus_check(reference, specific_locus, info):
    if specific_locus is None:
        return
    elif not isinstance(specific_locus, dict):
        info['errors'].append('The specific locus is not a dictionary.')
        return
    if reference['type'] == 'genbank':
        if 'lrg' in specific_locus['type']:
            info['errors'].append('LRG specific locus mentioned for genbank '
                                  'reference.')


def variants_check(model, info):
    pass
