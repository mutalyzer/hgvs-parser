import pytest

from mutalyzer_hgvs_parser.convert import to_model
from mutalyzer_hgvs_parser.hgvs_parser import _get_child
from lark.tree import Tree
from .test_convert import INSERTED, DESCRIPTIONS, VARIANTS, LOCATIONS, REFERENCES
from .test_protein import HGVS_NOMENCLATURE


@pytest.mark.parametrize(
    "description, start_rule, model",
    [
        # insert_location | insert_length - length
        ("10", "inserted", INSERTED["10"]),
        # variant_certain_repeat | variant_certain_substitution - substitution
        (
            "LRG_199p1:p.Trp24Cys",
            "description",
            HGVS_NOMENCLATURE["LRG_199p1:p.Trp24Cys"],
        ),
        # 2. variant_certain_repeat | variant_certain_substitution - repeat
        # 1. insert_location | insert_length - length
        ("PREF:p.Ala2[10]", "description", HGVS_NOMENCLATURE["PREF:p.Ala2[10]"]),
        # 2. variants_certain_variant_predicted | variants_predicted_variant_certain - variants_predicted
        # 1. variant_certain_repeat | variant_certain_substitution - substitution
        (
            "NP_003997.1:p.(Trp24Cys)",
            "description",
            HGVS_NOMENCLATURE["NP_003997.1:p.(Trp24Cys)"],
        ),
        # 2. variants_certain_variant_predicted | variants_predicted_variant_certain - variants_predicted
        # 1. variant_certain | variant_predicted - variant_predicted
        ("R1(R2(R3)):g.(10_15)", "description", DESCRIPTIONS["R1(R2(R3)):g.(10_15)"]),
        # insertion | repeat - insertion
        (
            "10_11insNM_000001.1:c.100_200",
            "variant",
            VARIANTS["10_11insNM_000001.1:c.100_200"],
        ),
        # deletion | deltion_insertion | repeat - deletion_insertion
        ("10_11delinsR2:g.10_15", "variant", VARIANTS["10_11delinsR2:g.10_15"]),
        # description_dna | description_protein - description_dna
        ("R1:g.10_11insA", "description", DESCRIPTIONS["R1:g.10_11insA"]),
        # variant_certain_locatio_and_substitution | variant_certain_location
        ("R1:10", "description", DESCRIPTIONS["R1:10"]),
    ],
)
def test_ambiguities(description, start_rule, model):
    assert to_model(description, start_rule) == model


@pytest.mark.parametrize(
    "children, path, output",
    [
        (
            [Tree("1", [Tree("2_1", []), Tree("2_2", [])])],
            [0],
            Tree("1", [Tree("2_1", []), Tree("2_2", [])]),
        ),
        ([Tree("1", [Tree("2_1", []), Tree("2_2", [])])], [0, 0], Tree("2_1", [])),
        ([Tree("1", [Tree("2_1", []), Tree("2_2", [])])], [0, 1], Tree("2_2", [])),
        ([Tree("1", [Tree("2_1", [])])], [0], Tree("1", [Tree("2_1", [])])),
        ([Tree("1", [Tree("2_1", [])])], [0, 0], Tree("2_1", [])),
    ],
)
def test_get_child(children, path, output):
    print(path)
    print(_get_child(children, path))
    assert _get_child(children, path) == output
