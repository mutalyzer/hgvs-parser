Library
=======

The `parse_description_to_model` can be used to convert an HGVS description
to a dictionary model.


```pycon
>>> from mutalyzer_hgvs_parser import parse_description_to_model
>>>
>>> model = parse_description_to_model('NG_012337.1(SDHD_v001):c.274G>T')
>>> model['reference']
{'id': 'NG_012337.1', 'selector': {'id': 'SDHD_v001'}}
```
