from stringology.lcs import llcs, lcsr, lcp


def test_lcs_equal():
    assert llcs('', '') == 0
    assert lcsr('', '') == 1
    assert lcp('', '') == 0
    assert llcs('abc', 'abc') == 3
    assert lcsr('abc', 'abc') == 1
    assert lcp('abc', 'abc') == 3


def test_lcs_all_diff():
    assert llcs('abc', 'def') == 0
    assert lcsr('abc', 'def') == 0
    assert llcs('', 'def') == 0
    assert lcsr('', 'def') == 0
    assert llcs('abc', '') == 0
    assert lcsr('abc', '') == 0


def test_lcs_repl():
    assert llcs('abc', 'a-c') == 2
    assert llcs('abc', '-bc') == 2
    assert llcs('abc', 'ab-') == 2
    assert llcs('abc', '-b-') == 1


def test_lcs_ins():
    assert llcs('abc', 'abc-') == 3
    assert llcs('abc', '-abc') == 3
    assert llcs('abc', '-abc-') == 3


def test_lcs_del():
    assert llcs('abc', 'ab') == 2
    assert llcs('abc', 'bc') == 2
    assert llcs('abc', 'b') == 1
