"""
Module for converting HGVS descriptions and lark parse trees
to their equivalent dictionary models.
"""

from lark import Token, Transformer
from lark.exceptions import VisitError

from .exceptions import NestedDescriptions
from .hgvs_parser import parse
from .util import get_only_value, to_dict


def to_model(description, start_rule=None):
    """
    Convert an  HGVS description, or parts of it, e.g., a location,
    a variants list, etc., if an appropriate alternative `start_rule`
    is provided, to a nested dictionary model.

    :arg str description: HGVS description.
    :arg str start_rule: Alternative start rule.
    :returns: Description dictionary model.
    :rtype: dict
    """
    parse_tree = parse(description, start_rule=start_rule)
    return parse_tree_to_model(parse_tree)


def parse_tree_to_model(parse_tree):
    """
    Convert a parse tree to a nested dictionary model.

    :arg lark.Tree parse_tree: HGVS description.
    :returns: Description dictionary model.
    :rtype: dict
    """
    try:
        model = Converter().transform(parse_tree)
    except VisitError as e:
        raise e.orig_exc

    return model[list(model)[0]]


class Converter(Transformer):
    def description(self, children):
        return {"description": get_only_value(children)}

    def description_dna(self, children):
        output = {"type": "description_dna"}
        output.update(to_dict(children))
        _predicted(output)
        return {"description_dna": output}

    def description_protein(self, children):
        output = {"type": "description_protein"}
        output.update(to_dict(children))
        _predicted(output)
        return {"description_protein": output}

    def reference(self, children):
        output = {}
        output.update(children[0])
        if len(children) == 2:
            output.update(children[0])
            output["selector"] = children[1]["reference"]
        return {"reference": output}

    def ID(self, name):
        return {"id": name.value}

    def COORDINATE_SYSTEM(self, name):
        return {"coordinate_system": name.value}

    def variants(self, children):
        return {"variants": [child["variant"] for child in children]}

    def variants_predicted(self, children):
        return {"variants_predicted": [child["variant"] for child in children]}

    def variant_certain(self, children):
        return {"variant_certain": to_dict(children)}

    def variant_predicted(self, children):
        output = {"variant": to_dict(children)}
        output["variant"]["predicted"] = True
        return output

    def variant(self, children):
        return {"variant": to_dict(children)}

    def conversion(self, children):
        output = {"type": "conversion", "source": "reference"}
        output.update(to_dict(children))
        return output

    def deletion(self, children):
        output = {"type": "deletion", "source": "reference"}
        if children:
            output["deleted"] = children[0]["inserted"]
        return output

    def deletion_insertion(self, children):
        output = {"type": "deletion_insertion", "source": "reference"}
        if len(children) == 1:
            output["inserted"] = children[0]["inserted"]
        if len(children) == 2:
            output["deleted"] = children[0]["inserted"]
            output["inserted"] = children[1]["inserted"]

        return output

    def duplication(self, children):
        output = {"type": "duplication", "source": "reference"}
        if children:
            output["inserted"] = children[0]["inserted"]
        return output

    def equal(self, children):
        output = {"type": "equal", "source": "reference"}
        output.update(to_dict(children))
        return output

    def insertion(self, children):
        output = {"type": "insertion", "source": "reference"}
        output.update(to_dict(children))
        return output

    def inversion(self, children):
        output = {"type": "inversion", "source": "reference"}
        output.update(to_dict(children))
        return output

    def repeat(self, children):
        output = {"type": "repeat", "source": "reference"}
        output.update(to_dict(children))
        return output

    def substitution(self, children):
        output = {"type": "substitution", "source": "reference"}
        if len(children) == 2:
            children[0]["source"] = "description"
            output["deleted"] = [children[0]]
            output["inserted"] = children[1]["inserted"]
        else:
            output.update(to_dict(children))
        return output

    def extension(self, children):
        output = {"type": "extension", "source": "reference"}
        output.update(to_dict(children))
        return output

    def frame_shift(self, children):
        output = {"type": "frame_shift", "source": "reference"}
        output.update(to_dict(children))
        return output

    def location(self, children):
        return {"location": get_only_value(children)}

    def point(self, children):
        output = {"type": "point"}
        for child in children:
            if isinstance(child, dict):
                output.update(child)
            elif isinstance(child, Token) and child.type == "NUMBER":
                output["position"] = int(child.value)
            elif isinstance(child, Token) and child.type == "CHROMOSOME_POINT":
                output["position"] = child.value
        return {"point": output}

    def uncertain_point(self, children):
        return {
            "uncertain_point": {
                "start": get_only_value([children[0]]),
                "end": get_only_value([children[1]]),
                "type": "range",
                "uncertain": True,
            }
        }

    def range(self, children):
        return {
            "range": {
                "start": get_only_value([children[0]]),
                "end": get_only_value([children[1]]),
                "type": "range",
            }
        }

    def exact_range(self, children):
        return {
            "start": get_only_value([self.point([children[0]])]),
            "end": get_only_value([self.point([children[1]])]),
            "type": "range",
        }

    def OFFSET(self, name):
        output = {}
        if "?" in name.value:
            output["uncertain"] = True
            if "+" in name.value:
                output["downstream"] = True
            elif "-" in name.value:
                output["upstream"] = True
        else:
            output["value"] = int(name.value)
        return {"offset": output}

    def OUTSIDE_CDS(self, name):
        output = {}
        if name.value == "*":
            output["outside_cds"] = "downstream"
        elif name.value == "-":
            output["outside_cds"] = "upstream"
        return output

    def UNKNOWN(self, name):
        return {"uncertain": True}

    def inserted(self, children):
        output = []
        for child in children:
            output.extend(child["insert"])
        return {"inserted": output}

    def insert(self, children):
        if len(children) > 1 and children[0].get("repeat_mixed"):
            return _insert_repeat_mixed(children)
        new_children = []
        for child in children:
            if child.get("description_dna") or child.get("description_protein"):
                new_children.append(get_only_value([child]))
            else:
                new_children.append(child)
        return _insert(new_children)

    def repeat_number(self, children):
        return {"repeat_number": self.length(children)["length"]}

    def repeat_mixed(self, children):
        output = to_dict(children)
        if output.get("sequence"):
            output["source"] = "description"
        elif output.get("location"):
            output["source"] = "reference"
        return {"repeat_mixed": output}

    def INVERTED(self, name):
        return {"inverted": True}

    def length(self, children):
        length = children[0]
        if isinstance(length, Token) and length.type == "NUMBER":
            return {"length": {"type": "point", "value": int(length.value)}}
        if isinstance(length, dict):
            if length.get("type") == "range":
                length["uncertain"] = True
                if length["start"].get("uncertain") is None:
                    length["start"]["value"] = length["start"]["position"]
                    length["start"].pop("position")
                if length["end"].get("uncertain") is None:
                    length["end"]["value"] = length["end"]["position"]
                    length["end"].pop("position")
            elif length.get("uncertain"):
                length["type"] = "point"
            return {"length": length}

    def SEQUENCE(self, name):
        return {"sequence": name.value}

    def P_SEQUENCE(self, name):
        return {"sequence": name.value}

    def AA(self, name):
        return {"amino_acid": name.value}


def _predicted(model):
    """

    :param model:
    """
    if model.get("variants_predicted") is not None:
        model["variants"] = model["variants_predicted"]
        model["predicted"] = True
        model.pop("variants_predicted")


def _insert_repeat_mixed(children):
    """
    A repeat mixed ("AA[5]TTT[7]") is a list.
    """
    output = []
    for child in children:
        if child.get("repeat_mixed"):
            output.append(child["repeat_mixed"])
        else:
            raise Exception("Not repeat mixed.")
    return {"insert": output}


def _insert(children):
    output = to_dict(children)
    if output.get("sequence"):
        output["source"] = "description"
    elif output.get("location"):
        output["source"] = "reference"
    elif output.get("type"):
        if len(output["variants"]) != 1:
            raise NestedDescriptions()
        if len(output["variants"][0]) != 1:
            raise NestedDescriptions()
        output["source"] = output["reference"]
        output.update(output["variants"][0])
        output.pop("reference")
        output.pop("variants")
    return {"insert": [output]}
