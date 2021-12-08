from fractions import Fraction
import logging
from . import renderer


class Diagram:
    """
    A single crossingles matching with rational coefficient.

    An example of an instance:
    We think about the Diagram.id(2) with connections == [(0, 3), (1, 2)] and
    coefficient == 1 as:

        1 *
          0 1 2 3
          | \_/ |
          \_____/

    Sometimes we view the same diagram as:

        0 1
        | |
        | |
        3 2

    Calling `get_match(1)` on this would result in 2.

    `n: int`
            The integer n in 'crossingles matching on 2n vertices'.

    `_connections: list`
            A list of tuples (a, b) where a < b is a match.

    `_coefficient: Fraction`
            A Fraction
    """

    n: int
    _connections: list
    _coefficient: Fraction

    def __init__(self, connections: list = [(0, 1)], coefficient:Fraction = Fraction(1, 1)):
        # Some idiot testing
        if (not connections or
            not isinstance(connections, list) or
            not all(isinstance(match, tuple) for match in connections) or
            not all(len(match) == 2 for match in connections)):
            raise ValueError(f"`connections` must be a non-empty list of two element tuples: {connections}")

        if not (isinstance(coefficient, Fraction) or isinstance(coefficient, int)):
            raise ValueError(f"`coefficient` must be of type `Fraction` or `int`: `{type(coefficient).__name__}`")

        self.n = len(connections)
        self._connections = connections
        self._coefficient = coefficient

    def id(n):
        return Diagram(connections=[(a, 2 * n - a - 1) for a in range(n)])

    def U(n, i):
        if not i < n - 1:
            raise ValueError(f"`i` must be less than `n`-1 for U_i to exist in TL_n: {i}, {n}")

        connections = []

        for j in range(2 * n):
            if j == i:
                connections.append((i, i + 1))
            elif j == i + 1:
                continue
            elif j == 2 * n - (i + 1):
                connections.append((2 * n - (i + 1) - 1, 2 * n - i - 1))
            elif j == 2 * n - i:
                continue
            elif j < n:
                connections.append((j, 2 * n - j - 1))

        return Diagram(connections)

    def get_match(self, k):
        for match in self._connections:
            if match[0] == k:
                return match[1]
            elif match[1] == k:
                return match[0]

    def compose(self, diagram):
        """
        This takes `self` and stacks it on top of `diagram`.
        """

        coefficient = self._coefficient * diagram._coefficient
        connections = []

        # All indices from the perspective of `self`
        todo_top = list(range(self.n))
        todo_bottom = list(range(self.n, 2 * self.n))
        todo_middle = list(range(self.n, 2 * self.n))

        logging.info("todo_top:")
        logging.info(todo_top)
        logging.info("todo_bottom:")
        logging.info(todo_bottom)
        logging.info("todo_middle:")
        logging.info(todo_middle)

        # Run all string from the top
        while todo_top:
            i = todo_top.pop(0)
            logging.info(f"todo_top - {i}:")
            logging.info(todo_top)

            # Run through the combinded diagram until an end is reached
            apply_self = True
            j = i
            while True:
                if apply_self:
                    j = self.get_match(j)

                    # `self` leads back up
                    if j < self.n:
                        logging.info(f"todo_top - {j}:")
                        todo_top.remove(j)
                        logging.info(todo_top)
                        connections.append((i, j))
                        logging.info(connections)
                        logging.info("")
                        break
                    # `self` leads to the middle
                    else:
                        logging.info(f"todo_middle - {j}:")
                        todo_middle.remove(j)
                        logging.info(todo_middle)
                        apply_self = False
                else:
                    j = 2 * self.n - j - 1  # Re-indexing
                    j = diagram.get_match(j)

                    # `diagram` leads down
                    if j >= self.n:
                        logging.info(f"todo_bottom - {j}:")
                        todo_bottom.remove(j)
                        logging.info(todo_bottom)
                        connections.append((i, j))
                        logging.info(connections)
                        logging.info("")
                        break
                    # `diagram` leads back to the middle
                    else:
                        j = 2 * self.n - j - 1  # Re-indexing
                        logging.info(f"todo_middle - {j}:")
                        todo_middle.remove(j)
                        logging.info(todo_middle)
                        apply_self = True

        # Run all string from the bottom
        while todo_bottom:
            i = todo_bottom.pop(0)
            logging.info(f"todo_bottom - {i}:")
            logging.info(todo_bottom)

            # Run through the combinded diagram until an end is reached
            apply_self = False
            j = i
            while True:
                if not apply_self:
                    j = diagram.get_match(j)

                    # `diagram` leads back dowm
                    if j >= self.n:
                        logging.info(f"todo_bottom - {j}:")
                        todo_bottom.remove(j)
                        logging.info(todo_bottom)
                        connections.append((i, j))
                        logging.info(connections)
                        logging.info("")
                        break
                    # `diagram` leads to the middle
                    else:
                        j = 2 * self.n - j - 1  # Re-indexing
                        logging.info(f"todo_middle - {j}:")
                        todo_middle.remove(j)
                        logging.info(todo_middle)
                        apply_self = True
                else:
                    j = self.get_match(j)

                    # `self` leads up
                    if j < self.n:
                        assert False  # This can not happen because we already ran top down
                        logging.info(f"todo_top - {j}:")
                        todo_top.remove(j)
                        logging.info(todo_top)
                        connections.append((i, j))
                        logging.info(connections)
                        logging.info("")
                        break
                    # `self` leads back to the middle
                    else:
                        logging.info(f"todo_middle - {j}:")
                        todo_middle.remove(j)
                        logging.info(todo_middle)
                        apply_self = False
                        j = 2 * self.n - j - 1  # Re-indexing

        assert len(todo_middle) % 2 == 0

        for i in range(len(todo_middle) // 2):
            coefficient *= -2

        return Diagram(connections, coefficient)

    def tensor(self, other):
        """
        This takes `self` and puts it to the left of `other`.
        """

        other_offset = self.n
        self_right_half_offset = 2 * other.n

        connections = []

        for match in self._connections:
            i, j = match

            if i >= self.n:
                i += self_right_half_offset

            if j >= self.n:
                j += self_right_half_offset

            connections.append((i, j))

        for match in other._connections:
            i, j = match

            connections.append((i + other_offset, j + other_offset))

        return Diagram(connections, self._coefficient * other._coefficient)

    def _has_same_diagram_as(self, other, check_coefficient=False):
        if not self.n == other.n:
            return False

        # Compare the matches
        for match in self._connections:
            # assert isinstance(match, tuple)
            # assert len(str(match)) < 7
            # if str(match).startswith("\n"):
            #     assert False
            if match in other._connections:
                continue
            elif (match[1], match[0]) in other._connections:
                continue
            else:
                logging.info(f"{repr(self)} is not euqal to {repr(other)} because of {match} in {repr(self)}")
                return False

        return True

    def __eq__(self, other):
        # If there is a check against 0
        if (isinstance(other, int) or isinstance(other, Fraction) and
            other == 0):
            return self._coefficient == 0

        # Comapre the coefficients
        if not self._coefficient == other._coefficient:
            return False

        # Compare the actual diagrams
        return self._has_same_diagram_as(other, check_coefficient=True)

    def __and__(self, other):
        return self.tensor(other)

    __matmul__ = __and__

    def __mul__(self, other):
        # Diagram * other
        # => other is Diagram
        return self.compose(other)

    def __rmul__(self, other):
        # other * Diagram
        # and other is not Diagram (because __mul__ wans't called)
        # => other is scalar
        if isinstance(other, Fraction):
            return Diagram(connections=self._connections,
                           coefficient=other * self._coefficient)
        elif isinstance(other, int):
            return Fraction(other) * self

    def __add__(self, other):
        # Diagram + other
        # => other is Diagram
        assert self._has_same_diagram_as(other)

        return Diagram(self._connections, self._coefficient + other._coefficient)

    def __radd__(self, other):
        # other + Diagram
        # and other is not Diagram (because __add__ wasn't called)
        # => other is 0 (called by `sum`)
        return self

    def __repr__(self):
        return f"{self._coefficient} * {self._connections}"

    def __str__(self):
        return "\n" + renderer.render(self) + "\n"
