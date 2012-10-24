import pdb
import unittest
from protocols.bfg.bloom import BloomFilter, ErbBloomFilter

from configuration import FAST

class TestBloom(unittest.TestCase):
    """
    This class represents the expected behaviour to exist on
    a bloom filter.
    """

    def setUp(self):
        self.bloom_a = BloomFilter(m=100, k=4)
        self.bloom_a.add('one')
        self.bloom_a.add('two')
        self.bloom_a.add('three')
        self.bloom_a.add('four')
        self.bloom_a.add('five')

        self.bloom_b = BloomFilter(m=100, k=4)
        self.bloom_b.add('three')
        self.bloom_b.add('four')
        self.bloom_b.add('five')
        self.bloom_b.add('six')
        self.bloom_b.add('seven')
        self.bloom_b.add('eight')
        self.bloom_b.add('nine')
        self.bloom_b.add("ten")

    def test_duplicates_on_add(self):
        self.assertFalse(self.bloom_a.add('eleven'))
        self.assert_(self.bloom_a.add('eleven'))

    def test_membership_operation(self):
        assert 'ten' in self.bloom_b
        assert 'one' in self.bloom_a
        assert 'ten' not in self.bloom_a
        assert 'one' not in self.bloom_b

    def test_set_based_operation(self):
        union = self.bloom_b | self.bloom_a
        intersection = self.bloom_b & self.bloom_a

        assert 'ten' in union
        assert 'one' in union
        assert 'three' in intersection
        assert 'ten' not in intersection
        assert 'one' not in intersection

    def test_insertion(self):
        self.bloom_c = BloomFilter(m=100, k=4)
        self.bloom_c.add('one')
        self.assertTrue('one' in self.bloom_c)

    def test_filter_size(self):
        if FAST: return

        m = 100
        self.bloom_c = BloomFilter(m=m, k=4)
        self.assertEqual(self.bloom_c.m, m)

    def test_filter_hash_number(self):
        if FAST: return
        k = 4
        a = BloomFilter(m=100, k=k)
        self.assertEqual(a.k, k)

    def test_false_values(self):
        self.bloom_c = BloomFilter(m=100, k=4)
        self.assertFalse('two' in self.bloom_c)
        self.bloom_c.add('two')
        self.assertTrue('two' in self.bloom_c)
        self.bloom_c.add('two')
        self.assertFalse('one' in self.bloom_c)

    def test_equal_bits(self):
        if FAST: return

        self.bloom_c = BloomFilter(m=100, k=4)
        self.bloom_d = BloomFilter(m=100, k=4)
        self.bloom_c.add('one')
        self.bloom_d.add('one')
        self.assertEqual(self.bloom_c.bits, self.bloom_d.bits)

class TestERBBloom(unittest.TestCase):
    """
    This class represents the expected behaviour to exist on
    a ERB bloom filter.
    """

    def test_filter_removal_nodes(self):
        self.bloom_c = ErbBloomFilter(m=100, k=4)
        self.bloom_c.add('one')
        self.assertTrue('one' in self.bloom_c)
        if not FAST: #If the fast flag option is on, time doesn't pass for bloom filters
            self.bloom_c.pass_time()
            self.assertTrue('one' in self.bloom_c)
            self.bloom_c.pass_time()
            self.assertFalse('one' in self.bloom_c)

    def test_merge_filters(self):
        self.bloom_c = ErbBloomFilter(m=100, k=4)
        self.bloom_d = ErbBloomFilter(m=100, k=4)
        self.bloom_c.add('one')
        self.bloom_d.add('two')

        self.bloom_c = self.bloom_c.merge(self.bloom_d)

        self.assertTrue('one' in self.bloom_c and 'two' in self.bloom_c)
        self.assertTrue('one' not in self.bloom_d and 'two' in self.bloom_d)
