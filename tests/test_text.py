from stringology.text import remove_accents


def test_remove_accents():
    assert remove_accents("ãáà") == "aaa"
