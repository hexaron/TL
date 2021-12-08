import logging
from .diagram import Diagram
from .tl import TL
from .jones_wenzl import JW
from . import tl_tests
from . import diagram_tests
from . import renderer

# logging.basicConfig(level=logging.DEBUG)


# print("JW_3:", JW.get(3))
# print("JW_3^2:", JW.get(3) * JW.get(3))
#
# assert JW.get(4) * JW.get(4) == JW.get(4)

renderer.set_render_mode(renderer.DYCK_PATH)
print(TL.U(3, 0) * TL.U(3, 1))
