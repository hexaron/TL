"""
This module contains all the supported ways of turning a `Diagram` or `TL` into
a string.
"""

CORSSINGLESS_MATCHING = 0
DYCK_PATH = 1
STRING_DIAGRAM = 2


def set_render_mode(render_mode):
    RenderMode._render_mode = render_mode


def render(diagram):
    switch = {
        0: corssingless_matching,
        1: dyck_path,
        2: string_diagram
    }

    return switch[RenderMode._render_mode](diagram)


class RenderMode:
    # The default render mode
    _render_mode = CORSSINGLESS_MATCHING

"""
Some dang ASCII art.
"""


def string_diagram(diagram):
    n = diagram.n

    # There are numbers at the top and the bottom
    # They contain spaces in between
    size = n + (n - 1)

    coefficient = f"{diagram._coefficient} * "
    left_offset = "".join(" " for i in range(len(coefficient)))

    string = left_offset + "".join(str(i) + " " if len(str(i)) == 1 else str(i) for i in range(diagram.n))

    # A two dimensional grid of all the symbols to be placed
    symbols = [[" " for j in range(size)] for i in range(size)]

    for match in diagram._connections:
        i, j = min(match), max(match)

        # i on top
        if i < n:
            # j on top
            if j < n:
                # CASE: Cup
                for k in range(j - i):
                    symbols[k][2 * i + k] = "\\"
                    symbols[k][2 * j - k] = "/"

                symbols[j - i - 1][i + j] = "_"
            # j at bottom
            else:
                # CASE: String from top to bottom

                # Such a string consists of 3 parts:
                #  1. Vertical line
                #  2. Slanted segment (eventually)
                #  3. Vertical line

                # Flip j
                j = 2 * n - j - 1

                # The case where there is no slanted segment
                if i == j:
                    for k in range(size):
                        symbols[k][2 * i] = "|"
                else:
                    # We start by determining how long the slanted segment has
                    # to be
                    if i < j:
                        length = 2 * j - 2 * i + 1
                    else:
                        length = 2 * i - 2 * j + 1

                    # assert (size - length) % 2 == 0

                    vertical_lengths = (size - length) // 2

                    # 1.
                    for k in range(vertical_lengths):
                        symbols[k][2 * i] = "|"

                    # 3.
                    for k in range(vertical_lengths):
                        symbols[size - k - 1][2 * j] = "|"

                    # 2.
                    for k in range(length):
                        if i < j:
                            symbols[vertical_lengths + k][2 * i + k] = "\\"
                        else:
                            symbols[vertical_lengths + k][2 * i - k] = "/"
        # i at bottom
        else:
            # CASE: Cap

            # j at top cannot happen
            assert j >= n

            # Flip i and j
            i, j = 2 * n - j - 1, 2 * n - i - 1

            for k in range(j - i):
                symbols[size - k - 1][2 * i + k] = "/"
                symbols[size - k - 1][2 * j - k] = "\\"

            symbols[size - (j - i) - 1][i + j] = "_"


    for i in range(2 * n - 1):
        string += "\n"

        # Draw the coefficient in the vertical center
        if i == n - 1:
            string += coefficient + "".join(symbols[i])
        else:
            string += left_offset + "".join(symbols[i])

    string += "\n"

    string += left_offset + "".join(str(i) + " " if len(str(i)) == 1 else str(i) for i in range(2 * diagram.n - 1, n - 1, -1))

    return string


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
