import pdb
from BitVector import BitVector
from random import Random

# get hashes from http://www.partow.net/programming/hashfunctions/index.html
from hashes import RSHash, JSHash, PJWHash, ELFHash, DJBHash

from configuration import FAST


#
# ryan.a.cox@gmail.com / www.asciiarmor.com
#
# copyright (c) 2008, ryan cox
# all rights reserved 
# BSD license: http://www.opensource.org/licenses/bsd-license.php
#

class BloomFilter(object):
    """
    Implements the behaviour of a (normal) binary bloom filter
    """
    total_collisions_written = 0
    total_collisions_read = 0

    def __init__(self, m=None, k=None, bits=None ):
        """
        n --
        m -- Size (lenght) of the bloom filter array
        k -- number of hashes to use
        p -- 
        bits -- Bits to initialize the bloom filter (if empty all bits are 0)
        """
        self.debug_symbols = set([]) #TODO - To remove in the future
        if FAST: return

        self.m = m
        if k > 4 or k < 1:
            raise Exception('Must specify value of k between 1 and 4')
        self.k = k

        if bits:
            self.bits = bits
        else:
            self.bits = BitVector( size=m )

        self.rand = Random()
        self.hashes = []
        self.hashes.append(RSHash)
        self.hashes.append(JSHash)
        self.hashes.append(PJWHash)
        self.hashes.append(DJBHash)
        self.hashes.append(ELFHash)

        self._indexes = self._hash_indexes

    def __contains__(self, key):

        #### TODO - This is to remove ######
        if FAST:
            a = key in self.debug_symbols
            return a # In reality no bloom filters are being used
        ####################################

        for i in self._indexes(key):
            if not self.bits[i]:
                return False

        #### TODO - To Remove. Only usefull for debug ####
        if not key in self.debug_symbols:
            BloomFilter.total_collisions_read += 1
        #### --- To Remove ####

        return True

    def add(self, key):
        dupe = key in self.debug_symbols
        self.debug_symbols.add(key)
        if FAST: return dupe

        dupe = True
        bits = []
        for i in self._indexes(key): 
            if dupe and not self.bits[i]:
                dupe = False
            self.bits[i] = 1
            bits.append(i)

        return dupe

    def __and__(self, filter):
        if FAST:
            b = BloomFilter()
            b.debug_symbols = self.debug_symbols & filter.debug_symbols
            return b

        if (self.k != filter.k) or (self.m != filter.m):
            raise Exception('Must use bloom filters created with equal k' +
                            ' / m paramters for bitwise AND')
        bloom = BloomFilter(m=self.m, k=self.k, bits=(self.bits & filter.bits))
        bloom.debug_symbols = self.debug_symbols & filter.debug_symbols
        return bloom

    def __or__(self, filter):
        if FAST:
            b = BloomFilter()
            b.debug_symbols = self.debug_symbols | filter.debug_symbols
            return b

        if (self.k != filter.k) or (self.m != filter.m):
            raise Exception('Must use bloom filters created with equal k' +
                            '/ m paramters for bitwise OR')
        bloom = BloomFilter(m=self.m, k=self.k, bits=(self.bits | filter.bits))
        bloom.debug_symbols = self.debug_symbols | filter.debug_symbols
        return bloom

    def _hash_indexes(self, key):
        ret = []
        for i in range(self.k):
            ret.append(self.hashes[i](key) % self.m)
        return ret

    def _rand_indexes(self, key):
        self.rand.seed(hash(key))
        ret = []
        for i in range(self.k):
            ret.append(self.rand.randint(0, self.m-1))
        return ret

class ErbBloomFilter(BloomFilter):
    def __init__(self, m=None, k=None):
        """
        Don't know what will be different
        """
        BloomFilter.__init__(self, k=k, m=m)
        self.sticky = BloomFilter(k=k, m=m)

    def merge(self, filter):
        """
        Does an operation with another filter and store the result in
        both the plain and sticky filters

        filter -- The bloom filter to be ored
        """
        self.debug_symbols = self.debug_symbols | filter.debug_symbols

        if FAST: return self

        self.bits = filter.__or__(self).bits
        self.sticky = filter.__or__(self.sticky)
        return self

    def pass_time(self):
        if FAST: return

        self.bits = self.sticky.bits
        self.sticky = BloomFilter(k=self.k, m=self.m)

    def add(self, key):
        super(ErbBloomFilter, self).add(key)
        self.sticky.add(key)
