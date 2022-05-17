import unittest
import HashMapImmutable
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):
    def test_api(self):
        empty = HashMapImmutable.Hashdic()

        self.assertEqual(HashMapImmutable.to_list(HashMapImmutable.cons(empty, 1, None)), [None])
        l1 = HashMapImmutable.cons(HashMapImmutable.cons(empty, 1, 1), 2, None)
        l2 = HashMapImmutable.cons(HashMapImmutable.cons(empty, 2, None, ), 1, 1)
        self.assertEqual(HashMapImmutable.to_list(empty), [])
        self.assertTrue(str(HashMapImmutable.to_list(l1)) == "[None, 1]" or str(HashMapImmutable.to_list(l1)) == "[1, None]")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)
        self.assertEqual(l1, HashMapImmutable.cons(HashMapImmutable.cons(l1, 1, 1), 2, None))
        self.assertEqual(HashMapImmutable.length(empty), 0)
        self.assertEqual(HashMapImmutable.length(l1), 2)
        self.assertEqual(HashMapImmutable.length(l2), 2)
        self.assertEqual(str(HashMapImmutable.to_list(HashMapImmutable.remove(l1, 2))), "[1]")
        self.assertEqual(str(HashMapImmutable.to_list(HashMapImmutable.remove(l1, 1))), "[None]")
        self.assertFalse(HashMapImmutable.member(empty, 2))
        self.assertTrue(HashMapImmutable.member(l1, 2))
        self.assertTrue(HashMapImmutable.member(l1, 1))
        self.assertFalse(HashMapImmutable.member(l1, 3))

        self.assertTrue(HashMapImmutable.to_list(l1) == [None, 1] or HashMapImmutable.to_list(l1) == [1, None])
        self.assertEqual(l1, HashMapImmutable.from_list([1, None]))
        self.assertEqual(HashMapImmutable.mconcat(l1, l2), HashMapImmutable.from_list([1, None]))

        lst = HashMapImmutable.to_list(l1) + HashMapImmutable.to_list(l2)
        for e in l1.data:
            if e != l1.empty and e.key != -1:
                lst.remove(e.value)
        for e in l2.data:
            if e != l2.empty and e.key != -1:
                lst.remove(e.value)
        self.assertEqual(lst, [])

    def test_length(self):
        p = HashMapImmutable.Hashdic()
        self.assertEqual(HashMapImmutable.length(None), -1)
        p = HashMapImmutable.cons(p, 1, 5)
        self.assertEqual(HashMapImmutable.length(p), 1)
        p = HashMapImmutable.cons(p, 1025, 6)
        p = HashMapImmutable.cons(p, 2049, 9)
        self.assertEqual(HashMapImmutable.length(p), 3)

    def test_cons(self):
        p = HashMapImmutable.Hashdic()

        self.assertRaises(Exception, HashMapImmutable.cons, (p, None, 5))
        self.assertEqual(
            HashMapImmutable.cons(
                HashMapImmutable.cons(
                    p, "a", 5), 2, 6),
            HashMapImmutable.cons(
                HashMapImmutable.cons(
                    p, "a", 5), 2, 6))
        self.assertEqual(
            HashMapImmutable.cons(
                p, 1, 5), HashMapImmutable.cons(
                p, 1, 5))
        self.assertEqual(HashMapImmutable.cons(p, 1, 5),
                         HashMapImmutable.cons(p, 1, 5))

    def test_remove(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 2, 7)
        self.assertRaises(Exception, HashMapImmutable.remove, (p, None))
        self.assertRaises(Exception, HashMapImmutable.remove, (p, 7))
        self.assertEqual(
            HashMapImmutable.remove(
                p, 2), HashMapImmutable.cons(
                HashMapImmutable.Hashdic(), 1, 5))

    @given(a=st.lists(st.integers()))
    def test_monoid_identity(self, a: list):
        hash = HashMapImmutable.Hashdic()
        hash_a = HashMapImmutable.from_list(a)
        # a·empty and empty·a
        self.assertEqual(HashMapImmutable.mconcat(hash_a, HashMapImmutable.mempty(hash))
                         , HashMapImmutable.mconcat(HashMapImmutable.mempty(hash), hash_a))

    @given(b=st.integers(), d=st.integers(), f=st.integers())
    def test_monoid_associativity(self, b, d, f):
        emp = HashMapImmutable.Hashdic()
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 0, b)
        m = HashMapImmutable.Hashdic()
        q = HashMapImmutable.Hashdic()
        q = HashMapImmutable.cons(q, 1, d)
        m = HashMapImmutable.Hashdic()
        m = HashMapImmutable.cons(m, 0, b)
        m = HashMapImmutable.cons(m, 1, d)
        n = HashMapImmutable.Hashdic()
        n = HashMapImmutable.cons(n, 3, f)

        self.assertEqual(HashMapImmutable.mconcat(None, None), None)
        self.assertEqual(HashMapImmutable.mconcat(p, None), p)
        self.assertEqual(HashMapImmutable.mconcat(emp, emp), emp)
        self.assertEqual(HashMapImmutable.mconcat(p, emp), p)
        self.assertEqual(HashMapImmutable.mconcat(p, q), m)
        # (p·q)·n and p·(q·n)
        self.assertEqual(
            HashMapImmutable.mconcat(
                HashMapImmutable.mconcat(
                    p, q), n),
            HashMapImmutable.mconcat(
                p, HashMapImmutable.mconcat(
                    q, n)))

    @given(b=st.integers(), d=st.integers())
    def test_to_list(self, b, d):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, b)
        self.assertEqual(HashMapImmutable.to_list(None), [])
        self.assertEqual(HashMapImmutable.to_list(p), [b])
        p = HashMapImmutable.cons(p, 2, d)
        self.assertEqual(HashMapImmutable.to_list(p), [b, d])

    @given(a=st.integers())
    def test_from_list(self, a):
        test_data1 = [a]
        self.assertEqual(
            HashMapImmutable.to_list(
                HashMapImmutable.from_list(test_data1)),
            test_data1)

    def test_iter(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 2, 6)
        p = HashMapImmutable.cons(p, 3, 9)
        fun = HashMapImmutable.iterator(p)
        self.assertEqual(fun(), 5)
        self.assertEqual(fun(), 6)
        self.assertEqual(fun(), 9)
        self.assertEqual(fun(), -1)

    def test_find(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 2, 6)
        p = HashMapImmutable.cons(p, 3, 9)
        self.assertEqual(HashMapImmutable.find(p, 2), 6)
        self.assertEqual(HashMapImmutable.find(p, 1), 5)
        self.assertRaises(
            Exception, HashMapImmutable.find, (p, 5))

    def test_map(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 1026, 6)
        p = HashMapImmutable.cons(p, 2012, 9)

        def add(a):
            return a + 1
        self.assertEqual(HashMapImmutable.to_list(
            HashMapImmutable.map(p, add)), [6, 7, 10])

    def test_filter(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 1025, 6)
        p = HashMapImmutable.cons(p, 2049, 9)

        def is_even(a):
            return a % 2 == 0

        def is_odd(a):
            return a % 2 == 1
        self.assertEqual(HashMapImmutable.filter(p, is_even),  [5, 9])
        self.assertEqual(HashMapImmutable.filter(
            p, is_odd), [6])

    def test_reduce(self):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, 5)
        p = HashMapImmutable.cons(p, 2, 6)
        p = HashMapImmutable.cons(p, 3, 9)

        def sum(a, b):
            return a + b
        self.assertEqual(HashMapImmutable.reduce(p, sum, 0), 5 + 6 + 9)

    @given(b=st.integers())
    def test_immutability_check(self, b):
        p = HashMapImmutable.Hashdic()
        p1 = HashMapImmutable.cons(p, 3, b)
        self.assertNotEqual(id(p), id(p1))
        p2 = HashMapImmutable.remove(p1, 3)
        self.assertNotEqual(id(p1), id(p2))
        p3 = HashMapImmutable.mempty(p2)
        self.assertNotEqual(id(p2), id(p3))
        p4 = HashMapImmutable.mconcat(p, p1)
        self.assertNotEqual(id(p4), id(p))
        self.assertNotEqual(id(p4), id(p1))

        def add(a):
            return a + 1
        p5 = HashMapImmutable.map(p4, add)
        self.assertNotEqual(id(p5), id(p4))
