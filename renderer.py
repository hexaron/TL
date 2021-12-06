"""
This module contains all the supported ways of turning a `Diagram` or `TL` into
a string.
"""

CORSSINGLESS_MATCHING = 0
DYCK_PATH = 1


def set_render_mode(render_mode):
    RenderMode._render_mode = render_mode


def render(diagram):
    switch = {
        0: corssingless_matching,
        1: dyck_path
    }

    return switch[RenderMode._render_mode](diagram)


class RenderMode:
    # The default render mode
    _render_mode = CORSSINGLESS_MATCHING

"""
Some dang ASCII art.
"""


def dyck_path(diagram):
    string = f"{diagram._coefficient} ("

    # For each i in range(n) we can have a + or -
    symbols = [None for i in range(2 * diagram.n)]

    for match in diagram._connections:
        i, j = min(match), max(match)

        symbols[i] = "+"
        symbols[j] = "-"

    string += "".join(symbols)

    return string + ")"


def corssingless_matching(diagram):
    string = f"{diagram._coefficient} *\n  "

    string += "".join(str(i) + " " if len(str(i)) == 1 else str(i) for i in range(2 * diagram.n))

    for line in range(diagram.n):
        # Record which number wants which symbol below (i.e. " ", "|", "\" or "/")
        symbols = [None for i in range(2 * diagram.n)]

        for match in diagram._connections:
            i, j = min(match), max(match)

            if j - i - 1 < 2 * line:
                symbols[i] = " "
                symbols[j] = " "
            elif j - i - 1 > 2 * line:
                symbols[i] = "|"
                symbols[j] = "|"
            else:
                symbols[i] = "\\"
                symbols[j] = "/"

        if all([symbol == " " for symbol in symbols]):
            break

        # Add " " between each two symbols
        # Then split the list again for character replacement
        joined_symbol_list = list(" ".join(symbols))

        # We want to add "_" between "\" and "/"
        replace_underscore = False

        for i in range(len(joined_symbol_list)):
            if joined_symbol_list[i] == "\\":
                replace_underscore = True
            elif joined_symbol_list[i] == "/":
                replace_underscore = False
            # Do not replace "\" and "/"
            else:
                if replace_underscore:
                    joined_symbol_list[i] = "_"

        string += "\n  "
        string += "".join(joined_symbol_list)

    return string
