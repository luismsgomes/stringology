from stringology.ed import ed, ned, edsim


def test_ed_equal():
    assert ed('', '') == 0
    assert ned('', '') == 0
    assert edsim('', '') == 1
    assert ed('abc', 'abc') == 0
    assert ned('abc', 'abc') == 0
    assert edsim('abc', 'abc') == 1


def test_ed_all_diff():
    assert ed('abc', 'def') == 3
    assert ned('abc', 'def') == 1
    assert edsim('abc', 'def') == 0
    assert ed('', 'def') == 3
    assert ned('', 'def') == 1
    assert edsim('', 'def') == 0
    assert ed('abc', '') == 3
    assert ned('abc', '') == 1
    assert edsim('abc', '') == 0


def test_ed_repl():
    assert ed('abc', 'a-c') == 1
    assert ed('abc', '-bc') == 1
    assert ed('abc', 'ab-') == 1
    assert ed('abc', '-b-') == 2


def test_ed_ins():
    assert ed('abc', 'abc-') == 1
    assert ed('abc', '-abc') == 1
    assert ed('abc', '-abc-') == 2


def test_ed_del():
    assert ed('abc', 'ab') == 1
    assert ed('abc', 'bc') == 1
    assert ed('abc', 'b') == 2
