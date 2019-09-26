# Usage

This package provides a command line interface. To see the full options list,
use `-h`.

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
```

## Syntax check
To only check if a description can be successfully parsed.

```console
$ hgvsparser 'NG_012337.1(SDHD_v001):c.274G>T'
Successfully parsed:
 NG_012337.1(SDHD_v001):c.274G>T
```

## Variant description model
To also obtain the variant description model of the description, add the
`-c` flag.

```console
$ hgvsparser -c 'NG_012337.1(SDHD_v001):c.274G>T'
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
```

## Grammar start rule
By default, the Mutalyzer 3 grammar is employed, with the `description` start
rule. It is however possible to choose a different start rule.

```console
$ hgvsparser -r variant '274G>T'
Successfully parsed:
 274G>T
```
