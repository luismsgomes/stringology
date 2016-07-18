from stringology.lis import lis
from itertools import chain


def test_lis():
    assert lis([]) == []
    L = list(range(1000))
    assert lis(L) == L
    assert lis(L*3) == L
    R = list(reversed(L))
    assert len(lis(R)) == 1
    assert lis(L+R) == L
    assert lis(R+L) == L
    L2 = list(chain.from_iterable(zip(L, R)))
    assert lis(L2) == L
    L3 = [v*10 for v in L]
    assert lis(L3, indices=True) == L
