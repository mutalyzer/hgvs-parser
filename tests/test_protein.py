import pytest

from mutalyzer_hgvs_parser.protein import parse_protein, parse_protein_to_model

HGVS_NOMENCLATURE = {
    # Substitution
    # - missense
    "LRG_199p1:p.Trp24Cys": {
        "type": "description_protein",
        "reference": {"id": "LRG_199p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 24, "sequence": "Trp"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Cys", "source": "description"}],
            }
        ],
    },
    # - nonsense
    "NP_003997.1:p.(Trp24Cys)": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 24, "sequence": "Trp"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Cys", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    # - silent (no change)
    "NP_003997.1:p.Cys188=": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 188, "sequence": "Cys"},
                "type": "equal",
                "source": "reference",
            }
        ],
    },
    # - translation initiation codon
    #   - no protein
    "LRG_199p1:p.0": {},
    #   - unknown
    "LRG_199p1:p.Met1?": {},
    #   - new translation initiation site
    #     - downstream
    "NP_003997.1:p.Leu2_Met124del": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 2, "sequence": "Leu"},
                    "end": {"type": "point", "position": 124, "sequence": "Met"},
                },
                "type": "deletion",
                "source": "reference",
            }
        ],
    },
    #     - upstream
    "NP_003997.1:p.Met1_Leu2insArgSerThrVal": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 1, "sequence": "Met"},
                    "end": {"type": "point", "position": 2, "sequence": "Leu"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "ArgSerThrVal", "source": "description"}],
            }
        ],
    },
    #     - new
    "NP_003997.1:p.Met1ext-5": {},
    # - splicing
    "NP_003997.1:p.?": {},
    # - uncertain
    "NP_003997.1:p.(Gly56Ala^Ser^Cys)": {},
    # - mosaic
    "LRG_199p1:p.Trp24=/Cys": {},
    # Deletion
    # - one amino acid
    "LRG_199p1:p.Val7del": {
        "type": "description_protein",
        "reference": {"id": "LRG_199p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 7, "sequence": "Val"},
                "type": "deletion",
                "source": "reference",
            }
        ],
    },
    "LRG_199p1:p.(Val7del)": {
        "type": "description_protein",
        "reference": {"id": "LRG_199p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 7, "sequence": "Val"},
                "type": "deletion",
                "source": "reference",
            }
        ],
        "predicted": True,
    },
    "LRG_199p1:p.Trp4del": {
        "type": "description_protein",
        "reference": {"id": "LRG_199p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 4, "sequence": "Trp"},
                "type": "deletion",
                "source": "reference",
            }
        ],
    },
    # - several amino acids
    "NP_003997.1:p.Lys23_Val25del": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 23, "sequence": "Lys"},
                    "end": {"type": "point", "position": 25, "sequence": "Val"},
                },
                "type": "deletion",
                "source": "reference",
            }
        ],
    },
    "LRG_232p1:p.(Pro458_Gly460del)": {
        "type": "description_protein",
        "reference": {"id": "LRG_232p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 458, "sequence": "Pro"},
                    "end": {"type": "point", "position": 460, "sequence": "Gly"},
                },
                "type": "deletion",
                "source": "reference",
            }
        ],
        "predicted": True,
    },
    # -
    "LRG_232p1:p.Gly2_Met46del": {
        "type": "description_protein",
        "reference": {"id": "LRG_232p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 2, "sequence": "Gly"},
                    "end": {"type": "point", "position": 46, "sequence": "Met"},
                },
                "type": "deletion",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.Trp26Ter": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 26, "sequence": "Trp"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Ter", "source": "description"}],
            }
        ],
    },
    "PREF:p.Trp26*": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 26, "sequence": "Trp"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "*", "source": "description"}],
            }
        ],
    },
    # -
    "NP_003997.1:p.Val7=/del": {},
    # Duplication
    # -
    "PREF:p.Ala3dup": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 3, "sequence": "Ala"},
                "type": "duplication",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.(Ala3dup)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 3, "sequence": "Ala"},
                "type": "duplication",
                "source": "reference",
            }
        ],
        "predicted": True,
    },
    # -
    "PREF:p.Ala3_Ser5dup": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 3, "sequence": "Ala"},
                    "end": {"type": "point", "position": 5, "sequence": "Ser"},
                },
                "type": "duplication",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.Ser6dup": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 6, "sequence": "Ser"},
                "type": "duplication",
                "source": "reference",
            }
        ],
    },
    # Insertion
    # -
    "PREF:p.His4_Gln5insAla": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 4, "sequence": "His"},
                    "end": {"type": "point", "position": 5, "sequence": "Gln"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "Ala", "source": "description"}],
            }
        ],
    },
    # -
    "PREF:p.Lys2_Gly3insGlnSerLys": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 2, "sequence": "Lys"},
                    "end": {"type": "point", "position": 3, "sequence": "Gly"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "GlnSerLys", "source": "description"}],
            }
        ],
    },
    # -
    "PREF:p.(Met3_His4insGlyTer)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 3, "sequence": "Met"},
                    "end": {"type": "point", "position": 4, "sequence": "His"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "GlyTer", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    # -
    "PREF:p.Arg78_Gly79ins23": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 78, "sequence": "Arg"},
                    "end": {"type": "point", "position": 79, "sequence": "Gly"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"length": {"type": "point", "value": 23}}],
            }
        ],
    },
    # -
    # HGVS: "the in-frame insertion of a 62 amino acid sequence ending at a
    # stop codonat position *63 between amino acids Gln746 and Lys747. NOTE:
    # it must be possible to deduce the inserted amino acid sequence from the
    # description given at DNA or RNA level" -> not compatible with the grammar.
    "NP_060250.2:p.Gln746_Lys747ins*63": {},
    # - incomplete descriptions (preferably use exact descriptions only)
    #   -
    "NP_003997.1:p.(Ser332_Ser333ins(1))": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 332, "sequence": "Ser"},
                    "end": {"type": "point", "position": 333, "sequence": "Ser"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"length": {"type": "point", "value": 1}}],
            }
        ],
        "predicted": True,
    },
    "NP_003997.1:p.(Ser332_Ser333insX)": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 332, "sequence": "Ser"},
                    "end": {"type": "point", "position": 333, "sequence": "Ser"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "X", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    #   -
    "NP_003997.1:p.(Val582_Asn583ins(5))": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 582, "sequence": "Val"},
                    "end": {"type": "point", "position": 583, "sequence": "Asn"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"length": {"type": "point", "value": 5}}],
            }
        ],
        "predicted": True,
    },
    "NP_003997.1:p.(Val582_Asn583insXXXXX)": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 582, "sequence": "Val"},
                    "end": {"type": "point", "position": 583, "sequence": "Asn"},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "XXXXX", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    # Deletion-insertion
    # -
    "PREF:p.Cys28delinsTrpVal": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 28, "sequence": "Cys"},
                "type": "deletion_insertion",
                "source": "reference",
                "inserted": [{"sequence": "TrpVal", "source": "description"}],
            }
        ],
    },
    # -
    "PREF:p.Cys28_Lys29delinsTrp": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 28, "sequence": "Cys"},
                    "end": {"type": "point", "position": 29, "sequence": "Lys"},
                },
                "type": "deletion_insertion",
                "source": "reference",
                "inserted": [{"sequence": "Trp", "source": "description"}],
            }
        ],
    },
    # -
    "PREF:p.(Pro578_Lys579delinsLeuTer)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 578, "sequence": "Pro"},
                    "end": {"type": "point", "position": 579, "sequence": "Lys"},
                },
                "type": "deletion_insertion",
                "source": "reference",
                "inserted": [{"sequence": "LeuTer", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    # -
    "NP_000213.1:p.(Val559_Glu561del)": {
        "type": "description_protein",
        "reference": {"id": "NP_000213.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 559, "sequence": "Val"},
                    "end": {"type": "point", "position": 561, "sequence": "Glu"},
                },
                "type": "deletion",
                "source": "reference",
            }
        ],
        "predicted": True,
    },
    # -
    "NP_003070.3:p.(Glu125_Ala132delinsGlyLeuHisArgPheIleValLeu)": {
        "type": "description_protein",
        "reference": {"id": "NP_003070.3"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "position": 125, "sequence": "Glu"},
                    "end": {"type": "point", "position": 132, "sequence": "Ala"},
                },
                "type": "deletion_insertion",
                "source": "reference",
                "inserted": [
                    {"sequence": "GlyLeuHisArgPheIleValLeu", "source": "description"}
                ],
            }
        ],
        "predicted": True,
    },
    # -
    "PREF:p.[Ser44Arg;Trp46Arg]": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 44, "sequence": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 46, "sequence": "Trp"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
        ],
    },
    # Alleles
    # - variants on one allele
    "NP_003997.1:p.[Ser68Arg;Asn594del]": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 68, "sequence": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 594, "sequence": "Asn"},
                "type": "deletion",
                "source": "reference",
            },
        ],
    },
    "NP_003997.1:p.[(Ser68Arg;Asn594del)]": {
        "type": "description_protein",
        "reference": {"id": "NP_003997.1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 68, "sequence": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 594, "sequence": "Asn"},
                "type": "deletion",
                "source": "reference",
            },
        ],
        "predicted": True,
    },
    # - variants on different alleles
    #   - homozygous
    "NP_003997.1:p.[Ser68Arg];[Ser68Arg]": {},
    "NP_003997.1:p.[(Ser68Arg)];[(Ser68Arg)]": {},
    "NP_003997.1:p.(Ser68Arg)(;)(Ser68Arg)": {},
    #   - heterozygous
    "NP_003997.1:p.[Ser68Arg];[Asn594del]": {},
    "NP_003997.1:p.(Ser68Arg)(;)(Asn594del)": {},
    "NP_003997.1:p.[(Ser68Arg)];[?]": {},
    "NP_003997.1:p.[Ser68Arg];[Ser68=]": {},
    #    - one allele encoding two proteins
    "NP_003997.1:p.[Lys31Asn: {},Val25_Lys31del]": {},
    # -
    "NP_003997.1:p.[Arg49=/Ser]": {},
    # -
    "NP_003997.1:p.[Arg49=//Ser]": {},
    # Repeated sequences
    # -
    "PREF:p.Ala2[10]": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 2, "sequence": "Ala"},
                "type": "repeat",
                "source": "reference",
                "inserted": [{"length": {"type": "point", "value": 10}}],
            },
        ],
    },
    # -
    "PREF:p.Ala2[10];[11]": {},
    # -
    "PREF:p.Gln18[23]": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 18, "sequence": "Gln"},
                "type": "repeat",
                "source": "reference",
                "inserted": [{"length": {"type": "point", "value": 23}}],
            },
        ],
    },
    # -
    "PREF:p.(Gln18)[(70_80)]": {},
    # Frame shift
    # -
    "PREF:p.Arg97ProfsTer23": {},
    "PREF:p.Arg97fs"
    # -
    "PREF:p.(Tyr4*)": {},
    # -
    "PREF:p.Glu5ValfsTer5": {},
    "PREF:p.Glu5fs": {},
    # -
    "PREF:p.Ile327Argfs*?": {},
    "PREF:p.Ile327fs": {},
    # -
    "PREF:p.Gln151Thrfs*9": {},
    "PREF:p.His150Hisfs*10": {},
    # Extension
    # -
    "PREF:p.Met1ext-5": {},
    # -
    "PREF:p.Met1_Leu2insArgSerThrVal": {},
    # -
    "PREF:p.Ter110GlnextTer17": {},
    "PREF:p.*110Glnext*17": {},
    # -
    "PREF:p.(Ter315TyrextAsnLysGlyThrTer)": {},
    "PREF:p.*315TyrextAsnLysGlyThr*": {},
    # -
    "PREF:p.Ter327Argext*?": {},
    "PREF:p.*327Argext*?": {},
}


@pytest.mark.parametrize(
    "description",
    HGVS_NOMENCLATURE.keys(),
)
def test_hgvs_protein_parse(description):
    if HGVS_NOMENCLATURE.get(description):
        assert parse_protein(description) is not None


@pytest.mark.parametrize(
    "description",
    HGVS_NOMENCLATURE.keys(),
)
def test_hgvs_protein_convert(description):
    if HGVS_NOMENCLATURE.get(description):
        assert parse_protein_to_model(description) == HGVS_NOMENCLATURE[description]
