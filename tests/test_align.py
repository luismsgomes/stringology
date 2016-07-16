from stringology.align import align, mismatches


def test_align_equal():
    assert align('', '') == ('', '')
    assert align('abc', 'abc') == ('abc', 'abc')


def test_align_all_diff():
    assert align('abc', 'def') == ('abc', 'def')
    assert align('abc', '') == ('abc', '   ')


def test_align_repl():
    assert align('abc', 'a-c') == ('abc', 'a-c')
    assert align('abc', '-bc') == ('abc', '-bc')
    assert align('abc', 'ab-') == ('abc', 'ab-')
    assert align('abc', '-b-') == ('abc', '-b-')


def test_align_ins():
    assert align('abc', 'abc-') == ('abc ', 'abc-')
    assert align('abc', '-abc') == (' abc', '-abc')
    assert align('abc', '-abc-') == (' abc ', '-abc-')


def test_align_del():
    assert align('abc', 'ab') == ('abc', 'ab ')
    assert align('abc', 'bc') == ('abc', ' bc')
    assert align('abc', 'b') == ('abc', ' b ')
