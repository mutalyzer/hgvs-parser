"""
Syntax tests for the lark based HGVS parser - taken from the previous
Mutalyzer tests.
"""

import pytest

from mutalyzer_hgvs_parser.hgvs_parser import HgvsParser


@pytest.fixture
def grammar():
    return HgvsParser()


@pytest.fixture
def parser(grammar):
    def parse(description):
        __tracebackhide__ = True
        parse_tree = grammar.parse(description)
        if parse_tree is None:
            pytest.fail("failed to parse `%s`:" % description)

    return parse


@pytest.mark.parametrize(
    "description",
    [
        "NC_000001.10:c.58del",
        "NM_002001.2:c.12del",
        "NR_026752.1:c.1621del",
        "AB026906.1:c.40del",
    ],
)
def test_ncbi_references(parser, description):
    """
    Parse example variants with NCBI references.
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "LRG_9:c.159del",
        "LRG_199:c.159del",
    ],
)
def test_lrg_references(parser, description):
    """
    Parse example variants with LRG references.
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "UD_136095285869:g.100del",
    ],
)
def test_ud_references(parser, description):
    """
    Parse example variants with UD references.
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "NG_012337.1(SDHD_v001):c.274G>T",
        "NG_012337.1(SDHD_i001):c.274G>T",
        "NG_012337.1(NM_003002.2):c.274G>T",
        "NC_000017.10(KRTAP2-4_v001):c.100del",
        "UD_136095285869(MIR1302-2_v001):c.3813del",
        "NC_000001.10(NM_002074.3):c.58del",
        "NC_012920.1(MT-ND1):m.3460del",
        "LRG_9t1:c.159del",
        "LRG_9p1:c.159del",
    ],
)
def test_references_with_specific_segments(parser, description):
    """
    Parse example variants with specifications to a specific annotated segment
    of a reference sequence that be given in parentheses directly after the
    reference sequence.
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "NM_002001.2:c.[12del;10_11insA]",
        # "NM_002001.2:c.[(12del)]",
        # "NM_002001.2:c.[(12del)?]",
        # "NM_002001.2:c.[(12del);(12del)]",
        # "NM_002001.2:c.[(12del;12del)]",
        # "NM_002001.2:c.[((12del)?;12del)?]",
    ],
)
def test_alleles(parser, description):
    """
    Parse .
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "NM_002001.2:c.15_16insA",
        "NM_002001.2:c.15_16insATC",
        "NM_002001.2:c.15_16ins[A]",
        "NM_002001.2:c.15_16ins[ATC]",
        "NM_002001.2:c.15_16ins28_39",
        "NM_002001.2:c.15_16ins[28_39]",
        "NM_002001.2:c.15_16ins[28_39;A]",
        "NM_002001.2:c.15_16ins[28_39;ATC]",
        "NM_002001.2:c.15_16ins[28_39;A;ATC]",
        "NM_002001.2:c.15_16ins28_39inv",
        "NM_002001.2:c.15_16ins[28_39inv]",
        "NM_002001.2:c.15_16ins[28_39inv;A]",
        "NM_002001.2:c.15_16ins[28_39inv;ATC]",
        "NM_002001.2:c.15_16ins[28_39inv;A;ATC]",
    ],
)
def test_parse_compound_insertion(parser, description):
    """
    Parse compound insertions.
    """
    parser(description)


@pytest.mark.parametrize(
    "description",
    [
        "NM_002001.2:c.12_17delinsA",
        "NM_002001.2:c.12_17delinsATC",
        "NM_002001.2:c.12_17delins[A]",
        "NM_002001.2:c.12_17delins[ATC]",
        "NM_002001.2:c.12_17delins28_39",
        "NM_002001.2:c.12_17delins[28_39]",
        "NM_002001.2:c.12_17delins[28_39;A]",
        "NM_002001.2:c.12_17delins[28_39;ATC]",
        "NM_002001.2:c.12_17delins[28_39;A;ATC]",
        "NM_002001.2:c.12_17delins28_39inv",
        "NM_002001.2:c.12_17delins[28_39inv]",
        "NM_002001.2:c.12_17delins[28_39inv;A]",
        "NM_002001.2:c.12_17delins[28_39inv;ATC]",
        "NM_002001.2:c.12_17delins[28_39inv;A;ATC]",
    ],
)
def test_parse_compound_delins(parser, description):
    """
    Parse compound deletion-insertions.
    """
    parser(description)
