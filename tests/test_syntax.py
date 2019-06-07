"""
Syntax tests for the lark based HGVS parser - taken from the HGVS website.
"""

import pytest

from hgvsparser.hgvs_parser import HgvsParser


@pytest.fixture
def grammar():
    return HgvsParser()


@pytest.fixture
def parser(grammar):
    def parse(description):
        __tracebackhide__ = True
        parse_tree = grammar.parse(description)
        if parse_tree is None:
            pytest.fail('failed to parse `%s`:' % description)

    return parse


@pytest.mark.parametrize('description', [
    'NC_000023.10:g.33038255C>A',
    'NG_012232.1(NM_004006.1):c.93+1G>T',
    'LRG_199t1:c.79_80delinsTT',
    'LRG_199t1:c.[79G>T;80C>T]',
    'NM_004006.1:c.[145C>T;147C>G]',
    'LRG_199t1:c.54G>H',
    'NM_004006.1:c.123=',
    # 'LRG_199t1:c.85=/T>C',
    # 'NM_004006.1:c.85=//T>C',
    'NG_012232.1:g.19del',
    'NG_012232.1:g.19_21del',
    'NG_012232.1(NM_004006.1):c.183_186+48del',
    'LRG_199t1:c.3921del',
    'LRG_199t1:c.1704+1del',
    'LRG_199t1:c.1813del',
    'NG_012232.1(NM_004006.1):c.4072-1234_5155-246del',
    'NG_012232.1(NM_004006.1):c.(4071+1_4072-1)_(5154+1_5155-1)del',
    'LRG_199t1:c.720_991del',
    'NG_012232.1(NM_004006.1):c.(?_-245)_(31+1_32-1)del',
    'NC_000023.11:g.(31060227_31100351)_(33274278_33417151)del',
    'NC_000023.11:g.(?_31120496)_(33339477_?)del',
    # 'NG_012232.1:g.19_21=/del',
    # 'NG_012232.1:g.19_21=//del',
    'NM_004006.2:c.20dup',
    'NC_000023.10:g.33229407_33229410dup',
    'NM_004006.2:c.20_23dup',
    'NC_000023.10:g.33229407_33229410dup',
    'LRG_199t1:c.260_264+48dup',
    'NC_000023.10:g.32862852_32862904dup',
    'LRG_199t1:c.3921dup',
    'LRG_199t1:c.1704+1dup',
    'LRG_199t1:c.1813dup',
    'LRG_199t1:c.4072-1234_5155-246dup',
    'LRG_199t1:c.720_991dup',
    'NG_012232.1(NM_004006.2):c.(4071+1_4072-1)_(5154+1_5155-1)dup',
    'NC_000023.10:g.(32381076_32382698)_(32430031_32456357)[3]',
    'LRG_199t1:c.(4071+1_4072-1)_(5154+1_5155-1)[3]',
    'LRG_199t1:c.(?_-127)_(31+1_32-1)dup',
    'NC_000023.11:g.(31060227_31100351)_(33274278_33417151)dup',
    'NC_000023.11:g.(?_31120496)_(33339477_?)dup',
    # 'NG_012232.1:g.19_21=/dup',
    # 'NG_012232.1:g.19_21=//dup',
    'NC_000023.10:g.32867861_32867862insT',
    'NM_004006.2:c.169_170insA',
    'NC_000023.10:g.32862923_32862924insCCT',
    'LRG_199t1:c.240_241insAGG',
    # 'NC_000023.10:g.32867907_32867908insL37425.1:23_361',
    'NM_004006.2:c.419_420ins[T;401_419]',
    'LRG_199t1:c.419_420ins[T;450_470;AGGG]',
    'NM_004006.2:c.849_850ins850_900inv',
    'NM_004006.2:c.900_901ins850_900inv',
    'LRG_199t1:c.940_941ins[885_940inv;A;851_883inv]',
    'NM_004006.2:c.940_941ins[903_940inv;851_885inv]',
    # 'NM_004006.2:c.(222_226)insG',
    # 'NC_000004.11:g.(3076562_3076732)ins(12)',
    'NC_000023.10:g.32717298_32717299insN',
    'NM_004006.2:c.761_762insN',
    'NM_004006.2:c.761_762insNNNNN',
    # 'NM_004006.1:c.761_762ins(5)',
    # 'NC_000023.10:g.32717298_32717299ins(100)',
    # 'NC_000023.10:g.32717298_32717299ins(80_120)',
    # 'NC_000023.10:g.32717298_32717299ins(?)',
    # 'g.?_?insNC_000023.10:(12345_23456)_(34567_45678)',
    'NC_000023.10:g.32361330_32361333inv',
    'NM_004006.2:c.5657_5660inv',
    'NM_004006.2:c.4145_4160inv',
    'NM_004006.2:c.849_850ins850_900inv',
    'NM_004006.2:c.900_901ins850_900inv',
    'LRG_199t1:c.940_941ins[885_940inv;A;851_883inv]',
    'NM_004006.2:c.940_941ins[903_940inv;851_885inv]',
    'NC_000022.10:g.42522624_42522669con42536337_42536382',
    # 'NC_000012.11:g.6128892_6128954conNC_000022.10:17179029_17179091',
    'NM_000797.3:c.812_829con908_925',
    'LRG_199t1:c.[2376G>C;3103del]',
    'NC_000023.10:g.[30683643A>G;33038273T>G]',
    # 'LRG_199t1:c.[2376G>C];[3103del]',
    # 'LRG_199t1:c.[296T>G;476T>C;1083A>C];[296T>G;1083A>C]',
    # 'LRG_199t1:c.[2376G>C];[2376=]',
    # 'LRG_199t1:c.[2376G>C];[?]',
    # 'LRG_199t1:c.2376G>C(;)3103del',
    # 'NM_004006.2:c.[296T>G;476T>C];[476T>C](;)1083A>C',
    # 'LRG_199t1:c.[296T>G];[476T>C](;)1083G>C(;)1406del',
    'NC_000014.8:g.101179660TG[14]',
    # 'NC_000014.8:g.101179660TG[14];[18]',
    'NM_023035.2(CACNA1A):c.6955CAG[26]',
    'NM_023035.2(CACNA1A):c.6955_6993dup',
    'LRG_763t1:c.54GCA[23]',
    # 'LRG_763t1:54_149GCA[23]ACA[1]GCC[2]ACC[1]GCC[10]',
    'NM_002024.5:c.-129CGG[79]',
    'NM_002024.5:c.-128GGM[108]',
    # 'NM_002024.5:c.(-231_-20)ins(1800_2400)',
    # 'NM_000492.3:c.1210-33_1210-6GT[11]T[6]',
    # 'NC_000012.11:g.112036755_112036823CTG[9]TTG[1]CTG[13]',
    'NC_000001.10:g.57832719ATAAA[15]',
    'NM_021080.3:c.-136-75952ATTTT[15]',
    'NG_012232.1:g.19=',
    'NG_012232.1:g.19_29=',
    # Other ones - for the open grammar
    'REF:[4]',
    # 'REF:1del[AAA;A[3]inv]insGGG[4]inv', TODO: -check if deleted = inserted
    'REF:10>[REF:g.(4_6)]',
    'REF:c.4conREF:g.[3;4;5;6;(5_5)_?con[3456_09209]]',
    'REF(A(B(C))):3'
])
def test_ncbi_references(parser, description):
    """
    Parse example variants with NCBI references.
    """
    parser(description)


@pytest.mark.parametrize('description', [
    ' NC_000023.10 : g . 33038255 C > A ',
    'LRG_199 t1 :c.( 4071+1_4072 -1)_ ( 5154 +1_5155-1)[ 3]',
])
def test_allowed_white_spaces(parser, description):
    """
    Parse example variants with NCBI references.
    """
    parser(description)