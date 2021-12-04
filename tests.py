from diagram import Diagram


def test(n = 3):
    test_a(n)
    print("\n\n\n")
    test_b(n)
    print("\n\n\n")
    test_c(n)


def test_a(n = 4):
    """
    For delta == -2:
    U_i^2 == delta * U_i
    """

    print("""\
+
| Running `test_a`:
|
|   U_i^2 = delta U_i,
|
| where delta = -2
+

""")

    U = [Diagram.U(n, i) for i in range(n - 1)]

    for i, u in enumerate(U):
        a, b = u.compose(u), -2 * u
        print(f"U_{i}^2:")
        print(a)
        print(f"-2 * U_{i}:")
        print(b)
        print()
        assert a == b


def test_b(n = 4):
    """
    U_i * U_{i+-1} * U_i == U_i
    """

    print("""\
+
| Running `test_b`:
|
|   U_i * U_{i+-1} * U_i = U_i.
+

""")

    U = [Diagram.U(n, i) for i in range(n - 1)]

    for i, u in enumerate(U):
        j = i - 1

        if j in range(len(U)):
            a, b = u.compose(U[j]).compose(u), u
            print(f"U_{i} * U_{{{i}-1}} * U_{i}:")
            print(a)
            print(f"U_{i}:")
            print(b)
            print()
            assert a == b

        j = i + 1

        if j in range(len(U)):
            a, b = u.compose(U[j]).compose(u), u
            print(f"U_{i} * U_{{{i}+1}} * U_{i}:")
            print(a)
            print(f"U_{i}:")
            print(b)
            print()
            assert a == b


def test_c(n = 4):
    """
    For |i - j| > 1:
    U_i * U_j == U_j * U_i
    """

    print("""\
+
| Running `test_c`:
|
|   U_i * U_j == U_j * U_i,
|
| for |i - j| > 1.
+

""")

    U = [Diagram.U(n, i) for i in range(n - 1)]

    for i, u in enumerate(U):
        for j, v in enumerate(U):
            if j - i > 1:
                a, b = u.compose(v), v.compose(u)
                print(f"U_{i} * U_{j}:")
                print(a)
                print(f"U_{j} * U_{i}:")
                print(b)
                print()
                assert a == b
            else:
                continue
