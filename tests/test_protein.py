import pytest

from mutalyzer_hgvs_parser.protein import parse_protein, parse_protein_to_model


@pytest.mark.parametrize(
    "description",
    [
        # Substitution
        # - missense
        "LRG_199p1:p.Trp24Cys",
        # - nonsense
        "NP_003997.1:p.(Trp24Cys)",
        # - silent (no change)
        "NP_003997.1:p.Cys188=",
        # - translation initiation codon
        #   - no protein
        "LRG_199p1:p.0",
        #   - unknown
        "LRG_199p1:p.Met1?",
        #   - new translation initiation site
        #     - downstream
        "NP_003997.1:p.Leu2_Met124del",
        #     - upstream
        "NP_003997.1:p.Met1_Leu2insArgSerThrVal",
        #     - new
        "NP_003997.1:p.Met1ext-5",
        # - splicing
        "NP_003997.1:p.?",
        # - uncertain
        "NP_003997.1:p.(Gly56Ala^Ser^Cys)",
        # - mosaic
        "LRG_199p1:p.Trp24=/Cys"
        # Deletion
        # - one amino acid
        "LRG_199p1:p.Val7del",
        "LRG_199p1:p.(Val7del)",
        "LRG_199p1:p.Trp4del",
        # - several amino acids
        "NP_003997.1:p.Lys23_Val25del",
        "LRG_232p1:p.(Pro458_Gly460del)",
        # -
        "LRG_232p1:p.Gly2_Met46del",
        # -
        "LRG_232p1:p.Trp26Ter",
        "LRG_232p1:p.Trp26*",
        # -
        "NP_003997.1:p.Val7=/del",
        # Duplication
        # -
        "PREF:p.Ala3dup",
        # -
        "PREF:p.(Ala3dup)",
        # -
        "PREF:p.Ala3_Ser5dup",
        # -
        "PREF:p.Ser6dup",
        # Insertion
        # -
        "PREF:p.His4_Gln5insAla",
        # -
        "PREF:p.Lys2_Gly3insGlnSerLys",
        # -
        "PREF:p.(Met3_His4insGlyTer)",
        # -
        "PREF:p.Arg78_Gly79ins23",
        # -
        "NP_060250.2:p.Gln746_Lys747ins*63",
        # - incomplete descriptions (preferably use exact descriptions only)
        #   -
        "NP_003997.1:p.(Ser332_Ser333ins(1))",
        "NP_003997.1:p.(Ser332_Ser333insX)",
        #   -
        "NP_003997.1:p.(Val582_Asn583ins(5))",
        "NP_003997.1:p.(Val582_Asn583insXXXXX)",
        # Deletion-insertion
        # -
        "PREF:p.Cys28delinsTrpVal",
        # -
        "PREF:p.Cys28_Lys29delinsTrp",
        # -
        "PREF:p.(Pro578_Lys579delinsLeuTer)",
        # -
        "NP_000213.1:p.(Val559_Glu561del)",
        # -
        "NP_003070.3:p.(Glu125_Ala132delinsGlyLeuHisArgPheIleValLeu)",
        # -
        "PREF:p.[Ser44Arg;Trp46Arg]",
        # Alleles
        # - variants on one allele
        "NP_003997.1:p.[Ser68Arg;Asn594del]",
        "NP_003997.1:p.[(Ser68Arg;Asn594del)]",
        # - variants on different alleles
        #   - homozygous
        "NP_003997.1:p.[Ser68Arg];[Ser68Arg]",
        "NP_003997.1:p.[(Ser68Arg)];[(Ser68Arg)]",
        "NP_003997.1:p.(Ser68Arg)(;)(Ser68Arg)",
        #   - heterozygous
        "NP_003997.1:p.[Ser68Arg];[Asn594del]",
        "NP_003997.1:p.(Ser68Arg)(;)(Asn594del)",
        "NP_003997.1:p.[(Ser68Arg)];[?]",
        "NP_003997.1:p.[Ser68Arg];[Ser68=]",
        #    - one allele encoding two proteins
        "NP_003997.1:p.[Lys31Asn,Val25_Lys31del]",
        # -
        "NP_003997.1:p.[Arg49=/Ser]",
        # -
        "NP_003997.1:p.[Arg49=//Ser]",
        # Repeated sequences
        # -
        "PREF:p.Ala2[10]",
        # -
        "PREF:p.Ala2[10];[11]",
        # -
        "PREF:p.Gln18[23]",
        # -
        "PREF:p.(Gln18)[(70_80)]",
        # Frame shift
        # -
        "PREF:p.Arg97ProfsTer23",
        "PREF:p.Arg97fs"
        # -
        "PREF:p.(Tyr4*)",
        # -
        "PREF:p.Glu5ValfsTer5",
        "PREF:p.Glu5fs",
        # -
        "PREF:p.Ile327Argfs*?",
        "PREF:p.Ile327fs",
        # -
        "PREF:p.Gln151Thrfs*9",
        "PREF:p.His150Hisfs*10",
        # Frame shift
        # -
        "PREF:p.Met1ext-5",
        # -
        "PREF:p.Met1_Leu2insArgSerThrVal",
        # -
        "PREF:p.Ter110GlnextTer17",
        "PREF:p.*110Glnext*17",
        # -
        "PREF:p.(Ter315TyrextAsnLysGlyThrTer)",
        "PREF:p.*315TyrextAsnLysGlyThr*",
        # -
        "PREF:p.Ter327Argext*?",
        "PREF:p.*327Argext*?",
    ],
)
def test_hgvs_protein_parse(description):
    assert parse_protein(description) is not None


@pytest.mark.parametrize(
    "tests",
    [
        # Substitution
        # - missense
        {
            "description": "LRG_199p1:p.Trp24Cys",
            "model": {
                "type": "description_protein",
                "reference": {"id": "LRG_199p1"},
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
        },
        # - nonsense
        {
            "descriptipon": "NP_003997.1:p.(Trp24Cys)",
            "model": {
                "type": "description_protein",
                "reference": {"id": "LRG_199p1"},
                "coordinate_system": "p",
                "variants": [
                    {
                        "location": {"type": "point", "position": 24},
                        "type": "substitution",
                        "source": "reference",
                        "inserted": [{"sequence": "Cys", "source": "description"}],
                    }
                ],
                "predicted": True,
            },
        },
        # - silent (no change)
        {
            "description": "NP_003997.1:p.Cys188=",
            "model": {
                "type": "description_protein",
                "reference": {"id": "NP_003997.1"},
                "coordinate_system": "p",
                "variants": [
                    {
                        "location": {"type": "point", "position": 188},
                        "type": "equal",
                        "source": "reference",
                    }
                ],
            },
        },
        # - translation initiation codon
        #   - no protein
        {"description": "LRG_199p1:p.0", "model": {}},
        #   - unknown
        {"description": "LRG_199p1:p.Met1?", "model": {}},
        #   - new translation initiation site
        #     - downstream
        {
            "description": "NP_003997.1:p.Leu2_Met124del",
            "model": {
                "type": "description_protein",
                "reference": {"id": "NP_003997.1"},
                "coordinate_system": "p",
                "variants": [
                    {
                        "location": {
                            "type": "range",
                            "start": {"type": "point", "position": 2},
                            "end": {"type": "point", "position": 124},
                        },
                        "type": "deletion",
                        "source": "reference",
                    }
                ],
            },
        },
        #     - upstream
        {"description": "NP_003997.1:p.Met1_Leu2insArgSerThrVal", "model": {}},
        #     - new
        {"description": "NP_003997.1:p.Met1ext-5", "model": {}},
        # - splicing
        {"description": "NP_003997.1:p.?", "model": {}},
        # - uncertain
        {"description": "NP_003997.1:p.(Gly56Ala^Ser^Cys)", "model": {}},
        # - mosaic
        "LRG_199p1:p.Trp24=/Cys"
        # Deletion
        # - one amino acid
        "LRG_199p1:p.Val7del",
        "LRG_199p1:p.(Val7del)",
        "LRG_199p1:p.Trp4del",
        # - several amino acids
        "NP_003997.1:p.Lys23_Val25del",
        "LRG_232p1:p.(Pro458_Gly460del)",
        # -
        "LRG_232p1:p.Gly2_Met46del",
        # -
        "LRG_232p1:p.Trp26Ter",
        "LRG_232p1:p.Trp26*",
        # -
        "NP_003997.1:p.Val7=/del",
        # Duplication
        # -
        "PREF:p.Ala3dup",
        # -
        "PREF:p.(Ala3dup)",
        # -
        "PREF:p.Ala3_Ser5dup",
        # -
        "PREF:p.Ser6dup",
        # Insertion
        # -
        "PREF:p.His4_Gln5insAla",
        # -
        "PREF:p.Lys2_Gly3insGlnSerLys",
        # -
        "PREF:p.(Met3_His4insGlyTer)",
        # -
        "PREF:p.Arg78_Gly79ins23",
        # -
        "NP_060250.2:p.Gln746_Lys747ins*63",
        # - incomplete descriptions (preferably use exact descriptions only)
        #   -
        "NP_003997.1:p.(Ser332_Ser333ins(1))",
        "NP_003997.1:p.(Ser332_Ser333insX)",
        #   -
        "NP_003997.1:p.(Val582_Asn583ins(5))",
        "NP_003997.1:p.(Val582_Asn583insXXXXX)",
        # Deletion-insertion
        # -
        "PREF:p.Cys28delinsTrpVal",
        # -
        "PREF:p.Cys28_Lys29delinsTrp",
        # -
        "PREF:p.(Pro578_Lys579delinsLeuTer)",
        # -
        "NP_000213.1:p.(Val559_Glu561del)",
        # -
        "NP_003070.3:p.(Glu125_Ala132delinsGlyLeuHisArgPheIleValLeu)",
        # -
        "PREF:p.[Ser44Arg;Trp46Arg]",
        # Alleles
        # - variants on one allele
        "NP_003997.1:p.[Ser68Arg;Asn594del]",
        "NP_003997.1:p.[(Ser68Arg;Asn594del)]",
        # - variants on different alleles
        #   - homozygous
        "NP_003997.1:p.[Ser68Arg];[Ser68Arg]",
        "NP_003997.1:p.[(Ser68Arg)];[(Ser68Arg)]",
        "NP_003997.1:p.(Ser68Arg)(;)(Ser68Arg)",
        #   - heterozygous
        "NP_003997.1:p.[Ser68Arg];[Asn594del]",
        "NP_003997.1:p.(Ser68Arg)(;)(Asn594del)",
        "NP_003997.1:p.[(Ser68Arg)];[?]",
        "NP_003997.1:p.[Ser68Arg];[Ser68=]",
        #    - one allele encoding two proteins
        "NP_003997.1:p.[Lys31Asn,Val25_Lys31del]",
        # -
        "NP_003997.1:p.[Arg49=/Ser]",
        # -
        "NP_003997.1:p.[Arg49=//Ser]",
        # Repeated sequences
        # -
        "PREF:p.Ala2[10]",
        # -
        "PREF:p.Ala2[10];[11]",
        # -
        "PREF:p.Gln18[23]",
        # -
        "PREF:p.(Gln18)[(70_80)]",
        # Frame shift
        # -
        "PREF:p.Arg97ProfsTer23",
        "PREF:p.Arg97fs"
        # -
        "PREF:p.(Tyr4*)",
        # -
        "PREF:p.Glu5ValfsTer5",
        "PREF:p.Glu5fs",
        # -
        "PREF:p.Ile327Argfs*?",
        "PREF:p.Ile327fs",
        # -
        "PREF:p.Gln151Thrfs*9",
        "PREF:p.His150Hisfs*10",
        # Frame shift
        # -
        "PREF:p.Met1ext-5",
        # -
        "PREF:p.Met1_Leu2insArgSerThrVal",
        # -
        "PREF:p.Ter110GlnextTer17",
        "PREF:p.*110Glnext*17",
        # -
        "PREF:p.(Ter315TyrextAsnLysGlyThrTer)",
        "PREF:p.*315TyrextAsnLysGlyThr*",
        # -
        "PREF:p.Ter327Argext*?",
        "PREF:p.*327Argext*?",
    ],
)
def test_hgvs_protein_convert(tests):
    if isinstance(tests, dict) and tests.get("model"):
        assert parse_protein_to_model(tests["description"]) == tests["model"]
    else:
        assert False
