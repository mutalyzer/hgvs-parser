import sys
from mutalyzer_hgvs_parser.hgvs_parser import parse
from mutalyzer_hgvs_parser.exceptions import UnexpectedCharacter, UnexpectedEnd, NestedDescriptions

ok = []
unexpected = []
ambigs = []
other = []

with open(sys.argv[1]) as file:
    for line in file:
        description = line.strip()
        try:
            parse(description)
        except UnexpectedCharacter:
            unexpected.append(description)
        except UnexpectedEnd:
            unexpected.append(description)
        except Exception as e:
            if "Ambiguity not solved." in str(e):
                ambigs.append(description)
            else:
                print("-----")
                print(description)
                print(e)
                other.append(description)
        else:
            ok.append(description)

print(f"OK         : {len(ok)}")
print(f"ambigs     : {len(ambigs)}")
print(f"unexpected : {len(unexpected)}")
print(f"other      : {len(other)}")

for ambig in ambigs:
    print(ambig)
