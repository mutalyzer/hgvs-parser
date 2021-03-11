Grammar
=======

The derived :download:`EBNF grammar <../mutalyzer_hgvs_parser/ebnf/hgvs_mutalyzer_3.g>`
does not consider all the HGVS_ nomenclature recommendations. Currently,
the focus is mostly on descriptions at the DNA level. Examples of
descriptions not supported:

- ``LRG_199t1:c.[2376G>C];[3103del]``
- ``LRG_199t1:c.2376G>C(;)3103del``
- ``NC_000002.12:g.pter_8247756delins[NC_000011.10:g.pter_15825272]``
- ``NC_000009.12:g.pter_26393001delins102425452_qterinv``
- ``NC_000011.10::g.1999904_1999946|gom``

At the same time, the grammar allows for descriptions which are not HGVS
compliant, but interpretable, in order to help users reach a normalized
description. Examples:

- ``LRG_1:g.20>T``
- ``LRG_1:g.20_40>70_80``
- ``LRG_1:g.20_23delAATG``
- ``NG_012337.1(NM_003002.2):274G>T``

.. _HGVS: https://varnomen.hgvs.org/