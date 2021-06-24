import pytest

from mutalyzer_hgvs_parser import parse, to_model

HGVS_NOMENCLATURE = {
    # Substitution
    # - missense
    "LRG_199p1:p.Trp24Cys": {
        "type": "description_protein",
        "reference": {"id": "LRG_199p1"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 24, "amino_acid": "Trp"},
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
                "location": {"type": "point", "position": 24, "amino_acid": "Trp"},
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
                "location": {"type": "point", "position": 188, "amino_acid": "Cys"},
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
                    "start": {"type": "point", "position": 2, "amino_acid": "Leu"},
                    "end": {"type": "point", "position": 124, "amino_acid": "Met"},
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
                    "start": {"type": "point", "position": 1, "amino_acid": "Met"},
                    "end": {"type": "point", "position": 2, "amino_acid": "Leu"},
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
                "location": {"type": "point", "position": 7, "amino_acid": "Val"},
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
                "location": {"type": "point", "position": 7, "amino_acid": "Val"},
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
                "location": {"type": "point", "position": 4, "amino_acid": "Trp"},
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
                    "start": {"type": "point", "position": 23, "amino_acid": "Lys"},
                    "end": {"type": "point", "position": 25, "amino_acid": "Val"},
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
                    "start": {"type": "point", "position": 458, "amino_acid": "Pro"},
                    "end": {"type": "point", "position": 460, "amino_acid": "Gly"},
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
                    "start": {"type": "point", "position": 2, "amino_acid": "Gly"},
                    "end": {"type": "point", "position": 46, "amino_acid": "Met"},
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
                "location": {"type": "point", "position": 26, "amino_acid": "Trp"},
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
                "location": {"type": "point", "position": 26, "amino_acid": "Trp"},
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
                "location": {"type": "point", "position": 3, "amino_acid": "Ala"},
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
                "location": {"type": "point", "position": 3, "amino_acid": "Ala"},
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
                    "start": {"type": "point", "position": 3, "amino_acid": "Ala"},
                    "end": {"type": "point", "position": 5, "amino_acid": "Ser"},
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
                "location": {"type": "point", "position": 6, "amino_acid": "Ser"},
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
                    "start": {"type": "point", "position": 4, "amino_acid": "His"},
                    "end": {"type": "point", "position": 5, "amino_acid": "Gln"},
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
                    "start": {"type": "point", "position": 2, "amino_acid": "Lys"},
                    "end": {"type": "point", "position": 3, "amino_acid": "Gly"},
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
                    "start": {"type": "point", "position": 3, "amino_acid": "Met"},
                    "end": {"type": "point", "position": 4, "amino_acid": "His"},
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
                    "start": {"type": "point", "position": 78, "amino_acid": "Arg"},
                    "end": {"type": "point", "position": 79, "amino_acid": "Gly"},
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
                    "start": {"type": "point", "position": 332, "amino_acid": "Ser"},
                    "end": {"type": "point", "position": 333, "amino_acid": "Ser"},
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
                    "start": {"type": "point", "position": 332, "amino_acid": "Ser"},
                    "end": {"type": "point", "position": 333, "amino_acid": "Ser"},
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
                    "start": {"type": "point", "position": 582, "amino_acid": "Val"},
                    "end": {"type": "point", "position": 583, "amino_acid": "Asn"},
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
                    "start": {"type": "point", "position": 582, "amino_acid": "Val"},
                    "end": {"type": "point", "position": 583, "amino_acid": "Asn"},
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
                "location": {"type": "point", "position": 28, "amino_acid": "Cys"},
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
                    "start": {"type": "point", "position": 28, "amino_acid": "Cys"},
                    "end": {"type": "point", "position": 29, "amino_acid": "Lys"},
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
                    "start": {"type": "point", "position": 578, "amino_acid": "Pro"},
                    "end": {"type": "point", "position": 579, "amino_acid": "Lys"},
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
                    "start": {"type": "point", "position": 559, "amino_acid": "Val"},
                    "end": {"type": "point", "position": 561, "amino_acid": "Glu"},
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
                    "start": {"type": "point", "position": 125, "amino_acid": "Glu"},
                    "end": {"type": "point", "position": 132, "amino_acid": "Ala"},
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
                "location": {"type": "point", "position": 44, "amino_acid": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 46, "amino_acid": "Trp"},
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
                "location": {"type": "point", "position": 68, "amino_acid": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 594, "amino_acid": "Asn"},
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
                "location": {"type": "point", "position": 68, "amino_acid": "Ser"},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Arg", "source": "description"}],
            },
            {
                "location": {"type": "point", "position": 594, "amino_acid": "Asn"},
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
                "location": {"type": "point", "position": 2, "amino_acid": "Ala"},
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
                "location": {"type": "point", "position": 18, "amino_acid": "Gln"},
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
    "PREF:p.Arg97ProfsTer23": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Arg", "position": 97},
                "type": "frame_shift",
                "source": "reference",
                "inserted": [
                    {"sequence": "Pro", "source": "description"},
                    {
                        "location": {"type": "point", "position": 23},
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    "PREF:p.Arg97fs": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Arg", "position": 97},
                "type": "frame_shift",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.(Tyr4*)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Tyr", "position": 4},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "*", "source": "description"}],
            }
        ],
        "predicted": True,
    },
    # -
    "PREF:p.Glu5ValfsTer5": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Glu", "position": 5},
                "type": "frame_shift",
                "source": "reference",
                "inserted": [
                    {"sequence": "Val", "source": "description"},
                    {
                        "location": {"type": "point", "position": 5},
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    "PREF:p.Glu5fs": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Glu", "position": 5},
                "type": "frame_shift",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.Ile327Argfs*?": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Ile", "position": 327},
                "type": "frame_shift",
                "source": "reference",
                "inserted": [
                    {"sequence": "Arg", "source": "description"},
                    {
                        "location": {"type": "point", "uncertain": True},
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    "PREF:p.Ile327fs": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Ile", "position": 327},
                "type": "frame_shift",
                "source": "reference",
            }
        ],
    },
    # -
    "PREF:p.Gln151Thrfs*9": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Gln", "position": 151},
                "type": "frame_shift",
                "source": "reference",
                "inserted": [
                    {"sequence": "Thr", "source": "description"},
                    {
                        "location": {"type": "point", "position": 9},
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    "PREF:p.His150Hisfs*10": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "His", "position": 150},
                "type": "frame_shift",
                "source": "reference",
                "inserted": [
                    {"sequence": "His", "source": "description"},
                    {
                        "location": {"type": "point", "position": 10},
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    # Extension
    # -
    "PREF:p.Met1ext-5": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Met", "position": 1},
                "type": "extension",
                "source": "reference",
                "inserted": [
                    {
                        "location": {
                            "type": "point",
                            "position": 5,
                            "outside_cds": "upstream",
                        },
                        "source": "reference",
                    }
                ],
            }
        ],
    },
    # -
    "PREF:p.Met1_Leu2insArgSerThrVal": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {
                    "type": "range",
                    "start": {"type": "point", "amino_acid": "Met", "position": 1},
                    "end": {"type": "point", "amino_acid": "Leu", "position": 2},
                },
                "type": "insertion",
                "source": "reference",
                "inserted": [{"sequence": "ArgSerThrVal", "source": "description"}],
            }
        ],
    },
    # -
    "PREF:p.Ter110GlnextTer17": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Ter", "position": 110},
                "type": "extension",
                "source": "reference",
                "inserted": [
                    {"sequence": "Gln", "source": "description"},
                    {
                        "location": {
                            "type": "point",
                            "amino_acid": "Ter",
                            "position": 17,
                        },
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    "PREF:p.*110Glnext*17": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "*", "position": 110},
                "type": "extension",
                "source": "reference",
                "inserted": [
                    {"sequence": "Gln", "source": "description"},
                    {
                        "location": {
                            "type": "point",
                            "amino_acid": "*",
                            "position": 17,
                        },
                        "source": "reference",
                    },
                ],
            }
        ],
    },
    # -
    "PREF:p.(Ter315TyrextAsnLysGlyThrTer)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "Ter", "position": 315},
                "type": "extension",
                "source": "reference",
                "inserted": [
                    {"sequence": "Tyr", "source": "description"},
                    {"sequence": "AsnLysGlyThrTer", "source": "description"},
                ],
            }
        ],
        "predicted": True,
    },
    "PREF:p.*315TyrextAsnLysGlyThr*": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "amino_acid": "*", "position": 315},
                "type": "extension",
                "source": "reference",
                "inserted": [
                    {"sequence": "Tyr", "source": "description"},
                    {"sequence": "AsnLysGlyThr*", "source": "description"},
                ],
            }
        ],
    },
    # -
    "PREF:p.Ter327Argext*?": {},
    "PREF:p.*327Argext*?": {},
}

OTHER = {
    "PREF:p.(=)": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [],
        "predicted": True,
    },
    "PREF:p.=": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [],
    },
    "PREF:p.24Cys": {
        "type": "description_protein",
        "reference": {"id": "PREF"},
        "coordinate_system": "p",
        "variants": [
            {
                "location": {"type": "point", "position": 24},
                "type": "substitution",
                "source": "reference",
                "inserted": [{"sequence": "Cys", "source": "description"}],
            }
        ],
    },
    # TODO: Should it be a protein or a dna description?
    # "PREF:24Cys": {
    #     "type": "description_protein",
    #     "reference": {"id": "PREF"},
    #     "coordinate_system": "p",
    #     "variants": [
    #         {
    #             "location": {"type": "point", "position": 24},
    #             "type": "substitution",
    #             "source": "reference",
    #             "inserted": [{"sequence": "Cys", "source": "description"}],
    #         }
    #     ],
    # },
}

TESTS = {**HGVS_NOMENCLATURE, **OTHER}


@pytest.mark.parametrize(
    "description",
    TESTS.keys(),
)
def test_hgvs_protein_parse(description):
    if TESTS.get(description):
        assert parse(description) is not None


@pytest.mark.parametrize(
    "description",
    TESTS.keys(),
)
def test_hgvs_protein_convert(description):
    if TESTS.get(description):
        assert to_model(description) == TESTS[description]
