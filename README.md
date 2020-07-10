# Mutalyzer HGVS Parser

Package to parse HGVS variant descriptions and to convert them into a
dictionary model.

It includes the original Mutalyzer `pyparsing` based implementation, for which
the EBNF grammar is written directly in Python, as well as the `lark` based
approach, which accepts the grammar written using the EBNF notation in a
separate file.

Please see [ReadTheDocs][RTD] for the latest documentation.

[RTD]: https://mutalyzer-hgvs-parser.readthedocs.io/en/latest/
