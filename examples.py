##############################
# Example from the "README.md"
##############################

from TL.tl import TL

# Get `U_2` in TL_4
U_2 = TL.U(4, 2)

# Print the string diagram of `U_2`
print(U_2)

U_1 = TL.U(4, 1)

# Print the composition of `U_1` and `U_2`
# (read right to left as usual)
print(U_1 * U_2)

# Print the tensor product of `U_1` and `U_2`
# (resulting in an element of TL_8)
print(U_1 & U_2)


########################
# Jones Wenzl projectors
########################

from TL.jones_wenzl import JW

# Print JW_2
print(JW.get(2))

# Print the composition of JW_2 with itself
print(JW.get(2) * JW.get(2))

# Check that they are equal
print(JW.get(2) == JW.get(2) * JW.get(2))


#################
# Custom diagrams
#################

from TL.diagram import Diagram
from fractions import Fraction

# Define a custom `Diagram` via a crossingles matching and a coefficient of -4
d_1 = Diagram([(0, 1), (2, 5), (4, 3)], -4)
print(d_1)

# Mulitply the identity consisting of 3 strings with the `Fraction` 3/5
d_2 = Fraction(3, 5) * Diagram.id(3)
print(d_2)

# To add `d_1` and `d_2` they need to be converted into a `TL`
tl_1 = TL([d_1])
tl_2 = TL([d_2])
print(tl_1 + tl_2)

# Another possibility is to just create a `TL` consisting of both diagrams
tl_sum = TL([d_1, d_2])
print(tl_sum)

# These approaches are equivalent
print(tl_1 + tl_2 == tl_sum)


###########################
# Choose different renderer
###########################

from TL import renderer

d = TL.U(3, 0) * TL.U(3, 1)

# Use crossingles matchings to represent diagrams
renderer.set_render_mode(renderer.CROSSINGLESS_MATCHING)
print(d)

# Use Dyck paths to represent diagrams
renderer.set_render_mode(renderer.DYCK_PATH)
print(d)

# Use the default (i.e. string diagrams) to represent diagrams
renderer.set_render_mode(renderer.STRING_DIAGRAM)
print(d)
