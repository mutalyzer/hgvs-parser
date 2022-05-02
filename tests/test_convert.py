"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from mutalyzer_hgvs_parser.convert import to_model
from mutalyzer_hgvs_parser.exceptions import NestedDescriptions


def _get_tests(tests):
    return [(k, tests[k]) for k in tests.keys()]


REFERENCES = {
    "R1": {"id": "R1"},
    "R1(R2)": {"id": "R1", "selector": {"id": "R2"}},
    "R1(R2(R3))": {"id": "R1", "selector": {"id": "R2", "selector": {"id": "R3"}}},
    "NM_000001.1": {"id": "NM_000001.1"},
    "NG_000001.1(NM_000002.3)": {
        "id": "NG_000001.1",
        "selector": {"id": "NM_000002.3"},
    },
}


@pytest.mark.parametrize("reference, model", _get_tests(REFERENCES))
def test_reference_to_model(reference, model):
    assert to_model(reference, "reference") == model


LOCATIONS = {
    "1": {"type": "point", "position": 1},
    "10": {"type": "point", "position": 10},
    "100": {"type": "point", "position": 100},
    "10-20": {"type": "point", "position": 10, "offset": {"value": -20}},
    "10+20": {"type": "point", "position": 10, "offset": {"value": +20}},
    "?": {"type": "point", "uncertain": True},
    "??": {"type": "point", "uncertain": True, "offset": {"uncertain": True}},
    "100?": {"type": "point", "position": 100, "offset": {"uncertain": True}},
    "?+?": {
        "type": "point",
        "uncertain": True,
        "offset": {"uncertain": True, "downstream": True},
    },
    "?-?": {
        "type": "point",
        "uncertain": True,
        "offset": {"uncertain": True, "upstream": True},
    },
    "-10": {"type": "point", "position": 10, "outside_cds": "upstream"},
    "-10-20": {
        "type": "point",
        "position": 10,
        "outside_cds": "upstream",
        "offset": {"value": -20},
    },
    "-10+20": {
        "type": "point",
        "position": 10,
        "outside_cds": "upstream",
        "offset": {"value": 20},
    },
    "*10": {"type": "point", "position": 10, "outside_cds": "downstream"},
    "*10+20": {
        "type": "point",
        "position": 10,
        "outside_cds": "downstream",
        "offset": {"value": 20},
    },
    "*10-20": {
        "type": "point",
        "position": 10,
        "outside_cds": "downstream",
        "offset": {"value": -20},
    },
    "10_15": {
        "type": "range",
        "start": {"type": "point", "position": 10},
        "end": {"type": "point", "position": 15},
    },
    "(10_15)": {
        "type": "range",
        "uncertain": True,
        "start": {"type": "point", "position": 10},
        "end": {"type": "point", "position": 15},
    },
    "(10_20)_30": {
        "type": "range",
        "start": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 10},
            "end": {"type": "point", "position": 20},
        },
        "end": {"type": "point", "position": 30},
    },
    "10_(20_30)": {
        "type": "range",
        "start": {"type": "point", "position": 10},
        "end": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 20},
            "end": {"type": "point", "position": 30},
        },
    },
    "(10_20)_(30_40)": {
        "type": "range",
        "start": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 10},
            "end": {"type": "point", "position": 20},
        },
        "end": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 30},
            "end": {"type": "point", "position": 40},
        },
    },
    "(?_-20)_(30+1_30-1)": {
        "type": "range",
        "start": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "uncertain": True},
            "end": {"type": "point", "position": 20, "outside_cds": "upstream"},
        },
        "end": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 30, "offset": {"value": 1}},
            "end": {"type": "point", "position": 30, "offset": {"value": -1}},
        },
    },
    "(?_-1)_(*1_?)": {
        "type": "range",
        "start": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "uncertain": True},
            "end": {"type": "point", "position": 1, "outside_cds": "upstream"},
        },
        "end": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "position": 1, "outside_cds": "downstream"},
            "end": {"type": "point", "uncertain": True},
        },
    },
    "(?_-1+?)_(*1-?_?)": {
        "type": "range",
        "start": {
            "type": "range",
            "uncertain": True,
            "start": {"type": "point", "uncertain": True},
            "end": {
                "type": "point",
                "position": 1,
                "outside_cds": "upstream",
                "offset": {"uncertain": True, "downstream": True},
            },
        },
        "end": {
            "type": "range",
            "uncertain": True,
            "start": {
                "type": "point",
                "position": 1,
                "outside_cds": "downstream",
                "offset": {"uncertain": True, "upstream": True},
            },
            "end": {"type": "point", "uncertain": True},
        },
    },
    "10_11": {
        "type": "range",
        "start": {"type": "point", "position": 10},
        "end": {"type": "point", "position": 11},
    },
    "10_20": {
        "type": "range",
        "start": {"type": "point", "position": 10},
        "end": {"type": "point", "position": 20},
    },
    "40_50": {
        "type": "range",
        "start": {"type": "point", "position": 40},
        "end": {"type": "point", "position": 50},
    },
    "200_300": {
        "type": "range",
        "start": {"type": "point", "position": 200},
        "end": {"type": "point", "position": 300},
    },
    "123_191": {
        "type": "range",
        "start": {"type": "point", "position": 123},
        "end": {"type": "point", "position": 191},
    },
    "(170_?)_420+60": {
        "type": "range",
        "start": {
            "type": "range",
            "start": {"type": "point", "position": 170},
            "end": {"type": "point", "uncertain": True},
            "uncertain": True,
        },
        "end": {"type": "point", "position": 420, "offset": {"value": 60}},
    },
    "pter": {
        "type": "point",
        "position": "pter",
    },
    "qter": {
        "type": "point",
        "position": "qter",
    },
    "pter_qter": {
        "type": "range",
        "start": {"type": "point", "position": "pter"},
        "end": {"type": "point", "position": "qter"},
    },
    "pter_100": {
        "type": "range",
        "start": {"type": "point", "position": "pter"},
        "end": {"type": "point", "position": 100},
    },
    "100_qter": {
        "type": "range",
        "start": {"type": "point", "position": 100},
        "end": {"type": "point", "position": "qter"},
    },
}


@pytest.mark.parametrize("description, model", _get_tests(LOCATIONS))
def test_location_to_model(description, model):
    assert to_model(description, "location") == model


LENGTHS = {
    "4": {"value": 4, "type": "point"},
    "5": {"value": 5, "type": "point"},
    "6": {"value": 6, "type": "point"},
    "10": {"value": 10, "type": "point"},
    "19": {"value": 19, "type": "point"},
    "20": {"type": "point", "value": 20},
    "?": {"uncertain": True, "type": "point"},
    "(10)": {"value": 10, "type": "point"},
    "(10_20)": {
        "type": "range",
        "uncertain": True,
        "start": {"type": "point", "value": 10},
        "end": {"type": "point", "value": 20},
    },
    "(?_20)": {
        "type": "range",
        "uncertain": True,
        "start": {"type": "point", "uncertain": True},
        "end": {"type": "point", "value": 20},
    },
}


@pytest.mark.parametrize("description, model", _get_tests(LENGTHS))
def test_length_to_model(description, model):
    assert to_model(description, "length") == model


INSERTED = {
    "A": [{"sequence": "A", "source": "description"}],
    "GA": [{"sequence": "GA", "source": "description"}],
    "10": [{"length": LENGTHS["10"]}],
    "(10)": [{"length": LENGTHS["(10)"]}],
    "(10_20)": [{"length": LENGTHS["(10_20)"]}],
    "(?_20)": [{"length": LENGTHS["(?_20)"]}],
    "10_20": [{"source": "reference", "location": LOCATIONS["10_20"]}],
    "[A;10_20]": [
        {"sequence": "A", "source": "description"},
        {"source": "reference", "location": LOCATIONS["10_20"]},
    ],
    "[A;?]": [
        {"sequence": "A", "source": "description"},
        {"length": LENGTHS["?"]},
    ],
    "[A;10_20inv]": [
        {"sequence": "A", "source": "description"},
        {"source": "reference", "location": LOCATIONS["10_20"], "inverted": True},
    ],
    "R2:g.10_15": [
        {
            "source": {"id": "R2"},
            "type": "description_dna",
            "coordinate_system": "g",
            "location": LOCATIONS["10_15"],
        }
    ],
    "NG_000001.1(NM_000002.3):c.100": [
        {
            "source": REFERENCES["NG_000001.1(NM_000002.3)"],
            "type": "description_dna",
            "coordinate_system": "c",
            "location": LOCATIONS["100"],
        }
    ],
    "NG_000001.1(NM_000002.3):c.(?_-20)_(30+1_30-1)": [
        {
            "source": REFERENCES["NG_000001.1(NM_000002.3)"],
            "type": "description_dna",
            "coordinate_system": "c",
            "location": LOCATIONS["(?_-20)_(30+1_30-1)"],
        }
    ],
    "NG_000001.1(NM_000002.3):c.(170_?)_420+60[19]": [
        {
            "source": REFERENCES["NG_000001.1(NM_000002.3)"],
            "type": "description_dna",
            "coordinate_system": "c",
            "location": LOCATIONS["(170_?)_420+60"],
            "repeat_number": LENGTHS["19"],
        }
    ],
    "[R2:g.200_300;40_50]": [
        {
            "source": {"id": "R2"},
            "type": "description_dna",
            "coordinate_system": "g",
            "location": LOCATIONS["200_300"],
        },
        {"source": "reference", "location": LOCATIONS["40_50"]},
    ],
    "[T;10_20inv;NM_000001.1:c.200_300]": [
        {"sequence": "T", "source": "description"},
        {"source": "reference", "location": LOCATIONS["10_20"], "inverted": True},
        {
            "source": {"id": "NM_000001.1"},
            "type": "description_dna",
            "coordinate_system": "c",
            "location": LOCATIONS["200_300"],
        },
    ],
    "qter": [
        {"source": "reference", "location": LOCATIONS["qter"]},
    ],
    "pter": [
        {"source": "reference", "location": LOCATIONS["pter"]},
    ],
    "pter_qter": [
        {"source": "reference", "location": LOCATIONS["pter_qter"]},
    ],
    "[pter_qter;10_20inv]": [
        {"source": "reference", "location": LOCATIONS["pter_qter"]},
        {"source": "reference", "location": LOCATIONS["10_20"], "inverted": True},
    ],
    "[pter_qterinv;10_20]": [
        {"source": "reference", "location": LOCATIONS["pter_qter"], "inverted": True},
        {"source": "reference", "location": LOCATIONS["10_20"]},
    ],
}

DELETED = {}


@pytest.mark.parametrize("description, model", _get_tests(INSERTED))
def test_inserted_to_model(description, model):
    assert to_model(description, "inserted") == model


VARIANTS = {
    "1": {"location": LOCATIONS["1"]},
    "??": {"location": LOCATIONS["??"]},
    "100?": {"location": LOCATIONS["100?"]},
    "10_15": {"location": LOCATIONS["10_15"]},
    "(10_15)": {"location": LOCATIONS["(10_15)"]},
    # Substitutions
    "10C>A": {
        "type": "substitution",
        "source": "reference",
        "location": LOCATIONS["10"],
        "deleted": [{"sequence": "C", "source": "description"}],
        "inserted": [{"sequence": "A", "source": "description"}],
    },
    "10>A": {
        "type": "substitution",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": INSERTED["A"],
    },
    "10>R2:g.10_15": {
        "type": "substitution",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": INSERTED["R2:g.10_15"],
    },
    "10>[R2:g.200_300;40_50]": {
        "type": "substitution",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": INSERTED["[R2:g.200_300;40_50]"],
    },
    # Deletions
    "10del": {"type": "deletion", "source": "reference", "location": LOCATIONS["10"]},
    "10delA": {
        "type": "deletion",
        "source": "reference",
        "location": LOCATIONS["10"],
        "deleted": [{"sequence": "A", "source": "description"}],
    },
    "10_15del6": {
        "type": "deletion",
        "source": "reference",
        "location": LOCATIONS["10_15"],
        "deleted": [{"length": {"value": 6, "type": "point"}}],
    },
    "pterdel": {
        "type": "deletion",
        "source": "reference",
        "location": LOCATIONS["pter"],
    },
    # Duplications
    "10dup": {
        "type": "duplication",
        "source": "reference",
        "location": LOCATIONS["10"],
    },
    "10dupG": {
        "type": "duplication",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": [{"sequence": "G", "source": "description"}],
    },
    # Insertions
    "10_11insA": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["A"],
    },
    "(10_11insA)": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["A"],
        "predicted": True,
    },
    "10_11ins[A]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["A"],
    },
    "10_11ins[A;10_20]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["[A;10_20]"],
    },
    "10_11ins[A;10_20inv]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["[A;10_20inv]"],
    },
    "10_11ins[T;10_20inv;NM_000001.1:c.200_300]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["[T;10_20inv;NM_000001.1:c.200_300]"],
    },
    "10_11ins[CAG[19]CAA[4]]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "10_11ins[CAG[19]CAA[4]10_20[19]]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
            {
                "location": LOCATIONS["10_20"],
                "source": "reference",
                "repeat_number": LENGTHS["19"],
            },
        ],
    },
    "10_11ins[CAG[19]10_20[19]CAA[4]]": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {
                "location": LOCATIONS["10_20"],
                "source": "reference",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "10_11insNM_000001.1:c.100_200": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": [
            {
                "source": {"id": "NM_000001.1"},
                "type": "description_dna",
                "coordinate_system": "c",
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 100},
                    "end": {"type": "point", "position": 200},
                },
            }
        ],
    },
    # TODO: Check if just a reference should be considered a description.
    # "10_11insNM_000001.1": {"type": "insertion",
    #                         "source": "reference",
    #                         "location": LOCATIONS["10_11"],
    #                         "inserted": [{"source": {"id": "NM_000001.1"}}]},
    "10_11insNG_000001.1(NM_000002.3):c.100": {
        "type": "insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": [
            {
                "source": {"id": "NG_000001.1", "selector": {"id": "NM_000002.3"}},
                "type": "description_dna",
                "coordinate_system": "c",
                "location": {"type": "point", "position": 100},
            }
        ],
    },
    # Inversions
    "10_11inv": {
        "type": "inversion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
    },
    "-10+20inv": {
        "type": "inversion",
        "source": "reference",
        "location": LOCATIONS["-10+20"],
    },
    "-10-20inv": {
        "type": "inversion",
        "source": "reference",
        "location": LOCATIONS["-10-20"],
    },
    # Conversions
    "10_20con40_50": {
        "type": "conversion",
        "source": "reference",
        "location": LOCATIONS["10_20"],
        "inserted": [{"source": "reference", "location": LOCATIONS["40_50"]}],
    },
    "10_20conR2:40_50": {
        "type": "conversion",
        "source": "reference",
        "location": LOCATIONS["10_20"],
        "inserted": [
            {
                "source": {"id": "R2"},
                "type": "description_dna",
                "location": LOCATIONS["40_50"],
            }
        ],
    },
    # Deletion insertions
    "10delinsGA": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": INSERTED["GA"],
    },
    "10_20delinsGA": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["10_20"],
        "inserted": INSERTED["GA"],
    },
    "10_20del10insGA": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["10_20"],
        "deleted": [{"length": {"value": 10, "type": "point"}}],
        "inserted": INSERTED["GA"],
    },
    "10delAinsGA": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["10"],
        "deleted": [{"sequence": "A", "source": "description"}],
        "inserted": INSERTED["GA"],
    },
    "10_11delinsR2:g.10_15": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["10_11"],
        "inserted": INSERTED["R2:g.10_15"],
    },
    "123_191delinsCAG[19]CAA[4]": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "123_191delinsCAG[19]invCAA[4]inv": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
                "inverted": True,
            },
            {
                "sequence": "CAA",
                "source": "description",
                "repeat_number": LENGTHS["4"],
                "inverted": True,
            },
        ],
    },
    "123_191delins[CAG[19]CAA[4]]": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "123_191delins[CAG[19];CAA[4]]": {
        "type": "deletion_insertion",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    # Repeats
    "10GA[20]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["10"],
        "inserted": [
            {"sequence": "GA", "source": "description", "repeat_number": LENGTHS["20"]}
        ],
    },
    "123_191CAG[19]CAA[4]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "123_191CAG[19]invCAA[4]inv": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
                "inverted": True,
            },
            {
                "sequence": "CAA",
                "source": "description",
                "repeat_number": LENGTHS["4"],
                "inverted": True,
            },
        ],
    },
    "123_191C[19]A[4]T[5]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {"sequence": "C", "source": "description", "repeat_number": LENGTHS["19"]},
            {"sequence": "A", "source": "description", "repeat_number": LENGTHS["4"]},
            {"sequence": "T", "source": "description", "repeat_number": LENGTHS["5"]},
        ],
    },
    "123_191C[19]10_20[19]A[4]T[5]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {"sequence": "C", "source": "description", "repeat_number": LENGTHS["19"]},
            {
                "location": LOCATIONS["10_20"],
                "source": "reference",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "A", "source": "description", "repeat_number": LENGTHS["4"]},
            {"sequence": "T", "source": "description", "repeat_number": LENGTHS["5"]},
        ],
    },
    "123_191[CAG[19];CAA[4]]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
        ],
    },
    "123_191[CAG[19];CAA[4];10_15[6]]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {"sequence": "CAA", "source": "description", "repeat_number": LENGTHS["4"]},
            {
                "location": LOCATIONS["10_15"],
                "source": "reference",
                "repeat_number": LENGTHS["6"],
            },
        ],
    },
    "123_191[CAG[19];CAA[4]inv;10_15[6]inv]": {
        "type": "repeat",
        "source": "reference",
        "location": LOCATIONS["123_191"],
        "inserted": [
            {
                "sequence": "CAG",
                "source": "description",
                "repeat_number": LENGTHS["19"],
            },
            {
                "sequence": "CAA",
                "source": "description",
                "repeat_number": LENGTHS["4"],
                "inverted": True,
            },
            {
                "location": LOCATIONS["10_15"],
                "source": "reference",
                "repeat_number": LENGTHS["6"],
                "inverted": True,
            },
        ],
    },
    # No changes (equal)
    # "=": [],
    "10=": {"type": "equal", "source": "reference", "location": LOCATIONS["10"]},
    "10_20=": {"type": "equal", "source": "reference", "location": LOCATIONS["10_20"]},
    "10del20": {
        "type": "deletion",
        "source": "reference",
        "location": LOCATIONS["10"],
        "deleted": [{"length": LENGTHS["20"]}],
    },
    "10del10_20": {
        "type": "deletion",
        "source": "reference",
        "location": LOCATIONS["10"],
        "deleted": [{"source": "reference", "location": LOCATIONS["10_20"]}],
    },
}


@pytest.mark.parametrize("variant, model", _get_tests(VARIANTS))
def test_variant_to_model(variant, model):
    assert to_model(variant, "variant") == model


@pytest.mark.parametrize(
    "variants, model",
    [("[{}]".format(";".join(VARIANTS.keys())), list(VARIANTS.values()))],
)
def test_variants_to_model(variants, model):
    assert to_model(variants, "variants") == model


DESCRIPTIONS = {
    "R1(R2(R3)):g.[10del;10_11delinsR2:g.10_15]": {
        "reference": REFERENCES["R1(R2(R3))"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [VARIANTS["10del"], VARIANTS["10_11delinsR2:g.10_15"]],
    },
    "R1(R2(R3)):g.([10del;10_11delinsR2:g.10_15])": {
        "reference": REFERENCES["R1(R2(R3))"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [VARIANTS["10del"], VARIANTS["10_11delinsR2:g.10_15"]],
        "predicted": True,
    },
    "R1(R2(R3)):g.(10_11delinsR2:g.10_15)": {
        "reference": REFERENCES["R1(R2(R3))"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [VARIANTS["10_11delinsR2:g.10_15"]],
        "predicted": True,
    },
    "R1(R2(R3)):g.(10_15)": {
        "reference": REFERENCES["R1(R2(R3))"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [VARIANTS["(10_15)"]],
    },
    "R1(R2(R3)):g.((10_15))": {
        "reference": REFERENCES["R1(R2(R3))"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [VARIANTS["(10_15)"]],
        "predicted": True,
    },
    "R1:g.[10=;10_11ins[T;10_20inv;NM_000001.1:c.200_300];10_20delinsGA]": {
        "reference": REFERENCES["R1"],
        "coordinate_system": "g",
        "type": "description_dna",
        "variants": [
            VARIANTS["10="],
            VARIANTS["10_11ins[T;10_20inv;NM_000001.1:c.200_300]"],
            VARIANTS["10_20delinsGA"],
        ],
    },
    "R1:10_11insA": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "variants": [VARIANTS["10_11insA"]],
    },
    "R1:10": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "variants": [{"location": LOCATIONS["10"]}],
    },
    "R1:-10+20inv": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "variants": [VARIANTS["-10+20inv"]],
    },
    "R1:-10-20inv": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "variants": [VARIANTS["-10-20inv"]],
    },
    "R1:10_20conR2:40_50": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "variants": [VARIANTS["10_20conR2:40_50"]],
    },
    "R1:g.10_20conR2:40_50": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "coordinate_system": "g",
        "variants": [VARIANTS["10_20conR2:40_50"]],
    },
    "R1:g.[10_20conR2:40_50;(10_11insA)]": {
        "reference": REFERENCES["R1"],
        "type": "description_dna",
        "coordinate_system": "g",
        "variants": [VARIANTS["10_20conR2:40_50"], VARIANTS["(10_11insA)"]],
    },
}


@pytest.mark.parametrize("description, model", _get_tests(DESCRIPTIONS))
def test_convert(description, model):
    assert to_model(description) == model


OPERATIONS_MIX = {
    ">": "substitution",
    "ins": "insertion",
    "delins": "deletion_insertion",
}


def compose_description_model(reference, location, operation, insert):
    description = "{}:{}{}{}".format(reference, location, operation, insert)
    model = {
        "reference": REFERENCES[reference],
        "type": "description_dna",
        "variants": [
            {
                "type": OPERATIONS_MIX[operation],
                "source": "reference",
                "location": LOCATIONS[location],
                "inserted": INSERTED[insert],
            }
        ],
    }
    return {description: model}


def _get_mix():
    descriptions = {}
    for operation in OPERATIONS_MIX:
        for reference in REFERENCES:
            for location in LOCATIONS:
                for insert in INSERTED:
                    descriptions.update(
                        compose_description_model(
                            reference, location, operation, insert
                        )
                    )
    return descriptions


@pytest.mark.parametrize("description, model", _get_tests(_get_mix()))
def test_mix(description, model):
    assert to_model(description) == model


@pytest.mark.parametrize(
    "description",
    ["R1:1delinsR2:2del", "R1:1del[R2:2del]", "R1:[1del;10_11insR2:2del]"],
)
def test_nested_descriptions(description):
    with pytest.raises(NestedDescriptions):
        to_model(description)
