from stringology.gaps import GappedKeywordMatcher


def test_gaps():
    search = GappedKeywordMatcher([
        [['A', 'B'], ['C']],
        [['A', 'B'], ['C'], ['D']],
        [['D', 'E']],
    ])
    text = 'A B x y C z D E'.split()
    expected = [
        ([['A', 'B'], ['C']], [0, 4]),
        ([['A', 'B'], ['C'], ['D']], [0, 4, 6]),
        ([['D', 'E']], [6]),
    ]
    found = list(search(text))
    assert found == expected
