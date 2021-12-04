from fractions import Fraction
import logging


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

    Sometimes we view the same diagram as a map like:

        0 1
        ^ ^
        | |
        3 2

    Calling `evaluate(0)` on this would result in 0, because 0 corresponds to 3.

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
        assert all([isinstance(match, tuple) for match in connections])

        self.n = len(connections)
        self._connections = connections
        self._coefficient = coefficient

    def id(n):
        return Diagram(connections=[(a, 2 * n - a - 1) for a in range(n)])

    def U(n, i):
        assert i < n - 1

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

    def evaluate(self, k):
        for match in self._connections:
            if match[1] == k:
                return match[0]
            elif match[0] == k:
                return match[1]

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
        while len(todo_top) > 0:
            i = todo_top.pop(0)
            logging.info(f"todo_top - {i}:")
            logging.info(todo_top)

            # Run through the combinded diagram until an end is reached
            apply_self = True
            j = i
            while True:
                if apply_self:
                    j = self.evaluate(j)

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
                    j = diagram.evaluate(j)

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
        while len(todo_bottom) > 0:
            i = todo_bottom.pop(0)
            logging.info(f"todo_bottom - {i}:")
            logging.info(todo_bottom)

            # Run through the combinded diagram until an end is reached
            apply_self = False
            j = i
            while True:
                if not apply_self:
                    j = diagram.evaluate(j)

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
                    j = self.evaluate(j)

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

    def __eq__(self, other):
        # Compare the connections
        if not self._coefficient == other._coefficient:
            return False

        for match in self._connections:
            if match in other._connections:
                continue
            elif (match[1], match[0]) in other._connections:
                continue
            else:
                print(f"{match}")
                return False

        return True

    def __rmul__(self, other):
        if isinstance(other, Diagram):
            return other.compose(self)
        elif isinstance(other, Fraction):
            return Diagram(connections=self._connections,
                           coefficient=self._coefficient * other)
        elif isinstance(other, int):
            return Fraction(other) * self

    def __repr__(self):
        return str(self._connections)

    def __str__(self):
        string = f"\n{self._coefficient} *\n  "

        string += " ".join(str(i) for i in range(2 * self.n))

        for line in range(self.n):
            # Record which number wants which symbol below (i.e. "|", "\" or "/")
            symbols = [None for i in range(2 * self.n)]

            for match in self._connections:
                if match[1] - match[0] - 1 < 2 * line:
                    symbols[match[0]] = " "
                    symbols[match[1]] = " "
                elif match[1] - match[0] - 1 > 2 * line:
                    symbols[match[0]] = "|"
                    symbols[match[1]] = "|"
                else:
                    symbols[match[0]] = "\\"
                    symbols[match[1]] = "/"

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

        return string + "\n"
