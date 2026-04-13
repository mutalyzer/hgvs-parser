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


An alternative start rule can be used to parse a partial description.
See :doc:`usage` for the list of available start rules.

.. code:: python

    >>> from mutalyzer_hgvs_parser import to_model
    >>> model = to_model('274del', 'variant')
    >>> model
    {'location': {'type': 'point', 'position': 274}, 'type': 'deletion', 'source': 'reference'}


The ``"source"`` field
----------------------

The ``"source"`` field indicates where a sequence or location originates:

``"description"``
    The sequence is written explicitly in the HGVS string.

    .. code:: python

        >>> to_model('274G>T', 'variant')['deleted']
        [{'sequence': 'G', 'source': 'description'}]

``"reference"``
    The sequence or location is implied by HGVS convention; it must be
    retrieved from the (same) reference sequence.

    .. code:: python

        >>> to_model('274del', 'variant')['source']
        'reference'

        >>> to_model('NG_012337.1:g.274_275ins100_200')['variants'][0]['inserted']
        [{'location': {...}, 'source': 'reference'}]

``{"id": "..."}``
    The sequence comes from an explicitly named external reference.

    .. code:: python

        >>> to_model('NG_012337.1:g.274_275insNG_012337.3:g.100_200')['variants'][0]['inserted']
        [{'type': 'description_dna', ..., 'source': {'id': 'NG_012337.3'}, ...}]


The ``parse()`` function
------------------------

The ``parse()`` function checks whether a description is syntactically valid
and raises an exception if not. Most users will want ``to_model()`` instead,
which both checks validity and returns the dictionary model in one step.
``parse()`` is useful when you only need to validate and do not need the model,
as it skips the conversion step.

.. code:: python

    >>> from mutalyzer_hgvs_parser import parse
    >>> parse("LRG_1:100del")
    Tree('description', ...)

The return value is a `lark Tree
<https://lark-parser.readthedocs.io/en/stable/classes.html#tree>`_ object.
Working with it directly requires familiarity with lark.


The ``HgvsParser`` class
------------------------

For advanced use cases, such as supplying a custom grammar file or controlling
whitespace handling, the ``HgvsParser`` class can be used directly. See the
:doc:`API documentation <api/hgvs_parser>` for details.

