Usage
=====

This package provides a :doc:`command line interface <cli>`.


Syntax check
------------

To only check if a description can be successfully parsed.

.. code-block:: console

    $ mutalyzer_hgvs_parser 'NG_012337.1(SDHD_v001):c.274G>T'
    Successfully parsed:
     NG_012337.1(SDHD_v001):c.274G>T


Description model
-----------------

To obtain the model of a description add the ``-c`` flag.

.. code-block:: console

    $ mutalyzer_hgvs_parser -c 'NG_012337.1(SDHD_v001):c.274G>T'
    {
      "reference": {
        "id": "NG_012337.1",
        "selector": {
          "id": "SDHD_v001"
        }
      },
      "coordinate_system": "c",
      "variants": [
        {
          "type": "substitution",
          "source": "reference",
          "location": {
            "type": "point",
            "position": 274
          },
          "deleted": [
            {
              "source": "description",
              "sequence": "G"
            }
          ],
          "inserted": [
            {
              "source": "description",
              "sequence": "T"
            }
          ]
        }
      ]
    }


Grammar start rule
------------------

By default, the Mutalyzer
:download:`grammar <../mutalyzer_hgvs_parser/ebnf/hgvs_mutalyzer_3.g>` is used,
with ``description`` as the start (top) rule. It is however possible
to choose a different start rule with the ``-r`` option.

.. code-block:: console

    $ mutalyzer_hgvs_parser -r variant '274G>T'
    Successfully parsed:
     274G>T

The ``-c`` flag can be employed together with a different start rule.

.. code-block:: console

    $ mutalyzer_hgvs_parser -c -r variant '274G>T'
    {
      "location": {
        "type": "point",
        "position": 274
      },
      "type": "substitution",
      "source": "reference",
      "deleted": [
        {
          "sequence": "G",
          "source": "description"
        }
      ],
      "inserted": [
        {
          "sequence": "T",
          "source": "description"
        }
      ]
    }


Parse tree representation
-------------------------

If pydot_ is installed, an image of the lark parse tree can be obtained
with the ``-i`` option.

.. code-block:: console

    $ mutalyzer_hgvs_parser "274del" -r variant -i tree.png
    Successfully parsed:
     274del
    Parse tree image saved to:
     tree.png

.. image:: images/tree.png
  :alt: Parse tree representation.

.. _pydot: https://pypi.org/project/pydot/
