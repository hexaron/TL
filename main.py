import logging
from tl import TL
import tl_tests
import diagram_tests

# logging.basicConfig(level=logging.DEBUG)

n = 4
U = [TL.U(n, i) for i in range(n - 1)]

print(U)
print(sum(U))
