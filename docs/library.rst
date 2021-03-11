Library
=======

The ``to_model()`` function can be used to convert an HGVS description
to a dictionary model.


.. code:: python

    >>> from mutalyzer_hgvs_parser import to_model
    >>> model = to_model('NG_012337.1(SDHD_v001):c.274G>T')
    >>> model['reference']
    {'id': 'NG_012337.1', 'selector': {'id': 'SDHD_v001'}}
