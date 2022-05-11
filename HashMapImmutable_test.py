import unittest
import HashMapImmutable
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):

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

    @given(a=st.integers(), b=st.integers(), c=st.integers(),
           d=st.integers(), e=st.integers(), f=st.integers())
    def test_mconcat(self, a, b, c, d, e, f):
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
        self.assertEqual(
            HashMapImmutable.mconcat(
                HashMapImmutable.mconcat(
                    p, q), n),
            HashMapImmutable.mconcat(
                p, HashMapImmutable.mconcat(
                    q, n)))

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_to_list(self, a, b, c, d):
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, 1, b)
        self.assertEqual(HashMapImmutable.to_list(None), [])
        self.assertEqual(HashMapImmutable.to_list(p), [b])
        p = HashMapImmutable.cons(p, 2, d)
        self.assertEqual(HashMapImmutable.to_list(p), [b, d])

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_from_list(self, a, b, c, d):
        test_data = []
        test_data1 = [b]
        test_data2 = [a, b, c, d]
        p = HashMapImmutable.Hashdic()
        p = HashMapImmutable.cons(p, a, b)
        self.assertRaises(
            Exception,
            HashMapImmutable.from_list, test_data)
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

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_immutability_check(self, a, b, c, d):
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
