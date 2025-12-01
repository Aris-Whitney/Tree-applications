from src.trie import Trie 


def test_insert_and_search():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("dog")

    assert t.search("cat")
    assert t.search("car")
    assert t.search("dog")
    assert not t.search("ca")
    assert not t.search("do")
    assert not t.search("cow")
    assert len(t) == 3


def test_starts_with_and_prefix():
    t = Trie()
    words = ["apple", "application", "applied", "apt", "bat"]
    for w in words:
        t.insert(w)

    assert t.starts_with("app")
    assert t.starts_with("ap")
    assert not t.starts_with("az")

    prefix_words = t.get_words_with_prefix("app")
    assert "apple" in prefix_words
    assert "application" in prefix_words
    assert "applied" in prefix_words
    assert "apt" not in prefix_words  # different prefix


def test_delete():
    t = Trie()
    t.insert("car")
    t.insert("card")
    t.insert("care")

    assert t.search("car")
    assert t.search("card")
    assert t.search("care")

    assert t.delete("card")
    assert not t.search("card")
    assert t.search("car")
    assert t.search("care")

    # deleting a non-existent word should return False
    assert not t.delete("cart")


def test_count_prefix():
    t = Trie()
    words = ["cat", "car", "cart", "dog"]
    for w in words:
        t.insert(w)

    assert t.count_prefix("ca") == 3
    assert t.count_prefix("car") == 2
    assert t.count_prefix("cart") == 1
    assert t.count_prefix("z") == 0
