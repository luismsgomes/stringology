from stringology.ngrams import all_ngrams


def test_ngrams():
    assert all_ngrams("") == []
    assert sorted(all_ngrams("abc")) == ["a", "ab", "abc", "b", "bc", "c"]
    assert sorted(all_ngrams(["a", "b", "c"])) == [
        ["a"],
        ["a", "b"],
        ["a", "b", "c"],
        ["b"],
        ["b", "c"],
        ["c"],
    ]
    assert sorted(all_ngrams("abc", maxn=2)) == ["a", "ab", "b", "bc", "c"]
    assert sorted(all_ngrams("abc", minn=2, maxn=2)) == ["ab", "bc"]
    assert sorted(all_ngrams("abc", minn=3, maxn=3)) == ["abc"]
    assert sorted(all_ngrams("abc", minn=1, maxn=1)) == ["a", "b", "c"]
    assert sorted(all_ngrams("abc", minn=2)) == ["ab", "abc", "bc"]
    assert sorted(all_ngrams("abc", minn=4)) == []
    assert sorted(all_ngrams("abc", maxn=0)) == []
