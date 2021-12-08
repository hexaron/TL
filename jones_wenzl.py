from fractions import Fraction
from .tl import TL


class JW:
    _cache = [TL.id(1)]

    def get(n):
        for i in range(n - len(JW._cache)):
            JW._calculate_step()

        return JW._cache[n - 1]

    def _calculate_step():
        # We want to calculate JW_n
        n = len(JW._cache) + 1

        jw = JW._cache[-1]

        # Now perform the recursive step
        jw_fat = jw & TL.id(1)
        jw_n = jw_fat + Fraction(n - 1, n) * jw_fat * TL.U(n, n - 2) * jw_fat

        JW._cache.append(jw_n)
