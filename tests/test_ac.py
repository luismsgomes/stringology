from stringology.ac import AhoCorasick


def test_ac():
    search = AhoCorasick([
        'a',
        'abc',
        'abcd',
        'abcdef',
        'abcdx',
        'ac',
        'bcd',
        'bcde',
        'bbcd',
    ])
    text = 'abcde'
    expected = [
        ('a', 0),
        ('abc', 0),
        ('abcd', 0),
        ('bcd', 1),
        ('bcde', 1),
    ]
    found = list(search(text))
    assert found == expected
