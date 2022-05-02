from lark.load_grammar import _TERMINAL_NAMES


class UnexpectedCharacter(Exception):
    def __init__(self, exception, description):
        self.line = exception.line
        self.column = exception.column
        self.allowed = exception.allowed
        self.considered_tokens = exception.considered_tokens
        self.pos_in_stream = exception.pos_in_stream
        self.state = exception.state
        self.unexpected_character = description[self.pos_in_stream]
        self.description = description
        self.expecting = _get_expecting(exception.allowed)

        message = "Unexpected character '{}' at position {}:\n".format(
            self.unexpected_character, self.column
        )
        message += self.get_context()
        message += "\nExpecting:"
        for expecting in self.expecting:
            message += "\n - {}".format(expecting)
        super(UnexpectedCharacter, self).__init__(message)

    def get_context(self):
        return "\n {}\n {}{}".format(self.description, " " * self.pos_in_stream, "^")

    def serialize(self):
        return {
            "line": self.line,
            "column": self.column,
            "pos_in_stream": self.pos_in_stream,
            "unexpected_character": self.unexpected_character,
            "description": self.description,
            "expecting": self.expecting,
        }


class UnexpectedEnd(Exception):
    def __init__(self, exception, description):
        self.pos_in_stream = len(description) - 1
        self.description = description
        lark_terminals = [terminal for terminal in exception.expected]
        self.expecting = _get_expecting(lark_terminals)

        message = "Unexpected character end of input"
        message += self.get_context()
        message += "\nExpecting:"
        for expecting in self.expecting:
            message += "\n - {}".format(expecting)
        super(UnexpectedEnd, self).__init__(message)

    def get_context(self):
        return "\n {}\n {}{}".format(self.description, " " * self.pos_in_stream, "^")

    def serialize(self):
        return {
            "pos_in_stream": self.pos_in_stream,
            "unexpected_character": self.description[-1],
            "description": self.description,
            "expecting": self.expecting,
        }


def _get_expecting(lark_terminal_list):
    expecting = set()
    for lark_terminal in lark_terminal_list:
        if TERMINALS.get(lark_terminal):
            expecting.add(TERMINALS[lark_terminal])
        else:
            expecting.add(lark_terminal)
    return list(expecting)


TERMINALS = {
    "ID": "a reference / selector ID",
    "COORDINATE_SYSTEM": "a coordinate system, e.g., 'g', 'o', 'm', 'c', 'n', 'r', or 'p'",
    "POSITION": "position (e.g., 100)",
    "OFFSET": "position offset ('-' or '+')",
    "OUTSIDE_CDS": "'*' or '-' for an outside CDS location",
    "DOT": "'.' between the coordinate system and the operation(s)",
    "COLON": "':' between the reference part and the coordinate system",
    "UNDERSCORE": "'_' between start and end in range or uncertain positions",
    "LPAR": "'(' for an uncertainty start or before a selector ID",
    "RPAR": "')' for an uncertainty end or after a selector ID",
    "SEMICOLON": "';' to separate variants",
    "LSQB": "'[' for multiple variants, insertions, or repeats",
    "RSQB": "']' for multiple variants, insertions, or repeats",
    "DEL": "deletion operation (e.g., 10del)",
    "DUP": "duplication operation (e.g., 10dup)",
    "INS": "insertion operation (e.g., 11_12insTA, ins10_20)",
    "CON": "conversion operation (e.g., 10_12con20_22)",
    "EQUAL": "'=' to indicate no changes",
    "DELETED": "deleted nucleotide in a substitution operation",
    "INSERTED": "inserted nucleotide in a substitution operation",
    "DELETED_SEQUENCE": "deleted sequence (e.g., ATG)",
    "DELETED_LENGTH": "deleted length (e.g., 50)",
    "DUPLICATED_SEQUENCE": "duplicated sequence (e.g., 'A')",
    "DUPLICATED_LENGTH": "duplicated length (e.g., 50)",
    "INVERTED": "inv",
    "INSERTED_SEQUENCE": "inserted sequence",
    "MORETHAN": "'>' in a substitution operation",
    "SEQUENCE": "sequence (e.g., ATG)",
    "REPEAT_LENGTH": "repeat length (e.g., 50)",
    "NT": "nucleotide, (e.g., 'A')",
    "NAME": "name",
    "LETTER": "a letter",
    "DIGIT": "a digit",
    "NUMBER": "a number (to indicate a location or a length)",
    "LCASE_LETTER": "lower case letter",
    "UCASE_LETTER": "upper case letter",
    "UNKNOWN": "?",
    "CHROMOSOME_POINT": "'pter' or 'qter'",
    "PREDICTED_EQUAL": "'(=)' for predicted no changes",
    "LPAR_LSQB": "'(['",
    "LSQB_LPAR": "'[('",
    "RSQB_RPAR": "'])'",
    "RPAR_RSQB": "')]'",
}


class NestedDescriptions(Exception):
    pass
