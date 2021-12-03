class Diagram:
    n: int
    _connections: list

    def __init__(self, n=2, connections=[]):
        self.n = n
        self._connections = connections

    def __str__(self):
        return str(self._connections)
