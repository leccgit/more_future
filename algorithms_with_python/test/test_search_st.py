import unittest

from algorithms_with_python.search_st.abs_st import AbsST
from algorithms_with_python.search_st.hash_st import ArrayHashST
from algorithms_with_python.search_st.symbol_st import SequentialSearchST, BinarySearchST


def test_main(hs: AbsST):
    hs.put("name", "lei")
    hs.put("age", "23")
    hs.put("age", "23")
    hs.put("age", "23")

    hs.put("like", "food")

    assert hs.contains("like") is True
    print(hs.size(), list(hs.keys()))
    assert hs.size() == 3
    hs.delete("age")
    for k in hs.keys():
        print(k, hs.get(k))
    for s in range(110):
        hs.put(s, "4")
    for s in range(110):
        hs.delete(s)

    assert hs.contains("like")
    print(list(hs.keys()))


class TestSearchST(unittest.TestCase):
    def test_sequential_searchSt(self):
        test_main(SequentialSearchST())

    def test_binary_searchSt(self):
        test_main(BinarySearchST())

    def test_array_hash_table(self):
        test_main(ArrayHashST())
