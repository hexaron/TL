from diagram import Diagram


class TL:
    """
    A Temperly-Lieb diagram, i.e. a linear combiniation of diagrams.

    `n`:
            From n to n vertices.
    `_diagrams`:
            A list of the included diagrams.
    `_coefficients`:
            A list of the corresponding coefficients (has the same order).
    """
    n: int
    _diagrams: list
    _coefficients: list

    def __init__(sef, n=2, diagrams=[Diagram.id(2)], coefficients=[1]):
