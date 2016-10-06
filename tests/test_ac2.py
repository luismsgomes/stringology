import pytest
from stringology.ac2 import AhoCorasick2


def test_ac2_search():
    automaton = AhoCorasick2([
        ('a', 1),
        ('abc', 2),
        ('abcd', 3),
        ('abcdef', 4),
        ('abcdx', 5),
        ('ac', 6),
        ('bcd', 7),
        ('bcde', 8),
        ('bbcd', 9),
    ])
    text = 'abcde'
    expected = [
        ((0, 1), 1),
        ((0, 3), 2),
        ((0, 4), 3),
        ((1, 4), 7),
        ((1, 5), 8),
    ]
    found = list(automaton(text))
    assert found == expected


def test_ac2_mutable_sequence_interface():
    items = [('AB', 1), ('ABC', 2), ('BC', 3), ('C', 4)]
    items = [(tuple(key), value) for key, value in items]
    keys = [k for k, v in items]
    values = [v for k, v in items]
    automaton = AhoCorasick2(items)
    assert sorted(automaton.items()) == sorted(items)
    assert sorted(automaton.keys()) == sorted(keys)
    assert sorted(automaton) == sorted(keys)
    assert sorted(automaton.values()) == sorted(values)
    with pytest.raises(ValueError):
        automaton['Z'] = None
    assert 'AB' in automaton
    # test the search functionality before mutation:
    assert list(automaton('ABCD')) == \
        [((0, 2), 1), ((0, 3), 2), ((1, 3), 3), ((2, 3), 4)]
    assert automaton['AB'] == 1
    assert len(automaton) == 4

    del automaton['AB']  # MUTATION

    assert len(automaton) == 3
    with pytest.raises(KeyError):
        automaton['Z']   # Z is not prefix of any pattern in automaton
    with pytest.raises(KeyError):
        automaton['AB']  # AB is prefix of pattern ABC in automaton
    with pytest.raises(KeyError):
        del automaton['Z']
    with pytest.raises(KeyError):
        del automaton['AB']
    assert 'Z' not in automaton
    assert 'AB' not in automaton
    assert sorted(automaton.values()) == [2, 3, 4]
    # test the search functionality after mutation:
    assert list(automaton('ABCD')) == \
        [((0, 3), 2), ((1, 3), 3), ((2, 3), 4)]

    del automaton['BC']  # this deletes a node that has a parent
    assert 'BC' not in automaton

    assert list(automaton('ABCD')) == \
        [((0, 3), 2), ((2, 3), 4)]
    assert sorted(automaton.keys()) == [tuple('ABC'), tuple('C')]
    assert sorted(automaton.values()) == [2, 4]

    automaton2 = AhoCorasick2()  # test empty init
    assert len(automaton2) == 0
    assert not automaton2.ready
    assert list(automaton2('ABCD')) == []
    assert automaton2.ready
    assert list(automaton2('ABCD')) == [] # calling for the second time
    assert 'Z' not in automaton2

    automaton2['A'] = 1
    assert len(automaton2) == 1
    automaton2['A'] = 2  # test re-assignment
    assert len(automaton2) == 1
    del automaton2['A']  # delete a node that is direct child of root
    assert len(automaton2) == 0
