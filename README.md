# HGVS Parser

Parser for HGVS variant descriptions.

It includes the original Mutalyzer `pyparsing` based implementation, for which
the EBNF grammar is written directly in Python, as well as the `lark` based
approach, which accepts the grammar written using the EBNF notation in a
separate file.

# Requirements

- Core requirements
  - Python 3.x
  - lark-parser
- Optional 
  - pyparsing (for the previous mutalyzer parser)
  - graphviz (for parse tree visualization)
- To run the tests
  - pytest


# Usage
```console
$ hgvsparser -h
usage: hgvsparser [-h] [-v] [-c] [-g G] [-r R] [-s S] [-p] description

hgvsparser: Parser for HGVS variant descriptions.

positional arguments:
  description  HGVS variant description to be parsed

optional arguments:
  -h, --help   show this help message and exit
  -v           show program's version number and exit
  -c           convert parse tree to model
  -g G         path to input grammar file
  -r R         start (top) rule for the grammar
  -s S         save parse tree as image
  -p           use the pyparsing parser

Copyright (c) 2018 Leiden University Medical Center <humgen@lumc.nl>
Copyright (c) 2018 Mihai Lefter <m.lefter@lumc.nl>
```


# Examples

## Successful parsing

```console
$ hgvsparser "NM_00000t1:g.[-1+3C>A;100_200del]" -t -c

Successfully parsed HGVS description:
 NM_00000:g.-1+3C>A

Equivalent model:
{
  "variants": [
    {
      "type": "substitution",
      "deleted": [
        {
          "sequence": "C",
          "source": "description"
        }
      ],
      "location": {
        "type": "point",
        "position": 1,
        "offset": 3,
        "outside_cds": "upstream"
      },
      "insertions": [
        {
          "sequence": "A",
          "source": "description"
        }
      ]
    },
    {
      "type": "del",
      "location": {
        "type": "range"
        "start": {
          "type": "point",
          "position": 100
        },
        "end": {
          "type": "point",
          "position": 200
        },
      }
    }

  ],
  "reference": {
    "type": "genbank",
    "accession": "NM_00000"
  },
  "coordinate_system": "g"
}

Model check summary:
{
  "warnings": "No version specified. The most recent found version will be considered.",
  "extras": [],
  "errors": [
    "LRG specific locus mentioned for genbank reference."
  ]
}
```

## Parsing errors


```console
$ hgvsparser "NM_00000:.-1+3C>A"
Error occured during parsing:
 No terminal defined for '.' at line 1 col 10

NM_00000:.-1+3C>A
         ^

Expecting: {
             Terminal('OUTSIDE_CDS'),
             Terminal('POSITION'),
             Terminal('LSQB'),
             Terminal('COORDINATE_SYSTEM'),
             Terminal('LPAR')
           }
```

```console
$ hgvsparser "NM_00000t1:g.100_200A>G" -t -c
Error occured during parsing:
 No terminal defined for 'A' at line 1 col 21

NM_00000t1:g.100_200A>G
                    ^

Expecting: {
             Terminal('DUP'),
             Terminal('OFFSET'),
             Terminal('LSQB'),
             Terminal('EQUAL'),
             Terminal('CON'),
             Terminal('DEL'),
             Terminal('INS'),
             Terminal('INVERTED')
           }
```

# Testing

```console
py.test tests
```
