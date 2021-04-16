Library
=======

The library provides a number of functions/classes to parse and convert descriptions.

The ``to_model()`` function
---------------------------

The ``to_model()`` function can be used to convert an HGVS description
to a dictionary model.

.. code:: python

    >>> from mutalyzer_hgvs_parser import to_model
    >>> model = to_model('NG_012337.1(SDHD_v001):c.274del')
    >>> model['reference']
    {'id': 'NG_012337.1', 'selector': {'id': 'SDHD_v001'}}


An alternative start rule for the grammar can be used.

.. code:: python

    >>> from mutalyzer_hgvs_parser import to_model
    >>> model = to_model('274del', 'variant')
    >>> model
    {'location': {'type': 'point', 'position': 274}, 'type': 'deletion', 'source': 'reference'}


The ``parse()`` function
------------------------

The ``parse()`` function can be used to parse for syntax correctness purposes
an HGVS description. Its output is a lark parse tree.

.. code:: python

    >>> from mutalyzer_hgvs_parser import parse
    >>> parse("LRG_1:100del")
    Tree('description', [Tree('reference', [Token('ID', 'LRG_1')]), Tree('variants',
    [Tree('variant', [Tree('location', [Tree('point', [Token('NUMBER', '100')])]), Tree('deletion', [])])])])

