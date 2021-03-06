#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class SipHash:
    """
    :category: Hash ID
    :rubric: PY
    :type: System
    :dsc:
        Generate a unique hash ID from the given string.
        This is supposed to be unique with a minimum expectation of collisions.
        This module is only in charge of producing the hash ID and the potential collisions should be monitored in the environment by the users
    """
    def __init__(self, c=2, d=4):
        assert c >= 0
        assert d >= 0
        self.__c = c
        self.__d = d

    def __process_message(self, message):
        self.__message = []

        length = len(message)
        for start in range(0, length - 7, 8):
            state = ord(message[start]) \
                | (ord(message[start + 1]) << 8)  \
                | (ord(message[start + 2]) << 16) \
                | (ord(message[start + 3]) << 24) \
                | (ord(message[start + 4]) << 32) \
                | (ord(message[start + 5]) << 40) \
                | (ord(message[start + 6]) << 48) \
                | (ord(message[start + 7]) << 56)
            self.__message.append(state)

        start = (length // 8) * 8
        state = (length % 256) << 56
        for i in range(length - start):
            state |= (ord(message[start + i]) << (i * 8))
        self.__message.append(state)

    def __SipRound(self):
        self.__v0 += self.__v1  # no need to mod 2^64 now
        self.__v2 += self.__v3
        self.__v1 = (self.__v1 << 13) | (self.__v1 >> 51)
        self.__v3 = (self.__v3 << 16) | (self.__v3 >> 48)
        self.__v1 ^= self.__v0
        self.__v3 ^= self.__v2
        self.__v0 = (self.__v0 << 32) | ((self.__v0 >> 32) & 0xffffffff)
        self.__v2 += self.__v1
        self.__v0 += self.__v3
        self.__v0 &= 0xffffffffffffffff
        self.__v1 = (self.__v1 << 17) | ((self.__v1 >> 47) & 0x1ffff)
        self.__v3 = ((self.__v3 & 0x7ffffffffff) << 21) \
            | ((self.__v3 >> 43) & 0x1fffff)
        self.__v1 ^= self.__v2
        self.__v1 &= 0xffffffffffffffff
        self.__v3 ^= self.__v0
        self.__v2 = ((self.__v2 & 0xffffffff) << 32) \
            | ((self.__v2 >> 32) & 0xffffffff)

    def auth(self, key, message):
        assert 0 <= key and key < 1 << 128
        k0 = key & 0xffffffffffffffff
        k1 = key >> 64

        # initialization
        self.__v0 = k0 ^ 0x736f6d6570736575
        self.__v1 = k1 ^ 0x646f72616e646f6d
        self.__v2 = k0 ^ 0x6c7967656e657261
        self.__v3 = k1 ^ 0x7465646279746573

        self.__process_message(message)

        # compression
        for m in self.__message:
            self.__v3 ^= m
            for i in range(self.__c):
                self.__SipRound()
            self.__v0 ^= m

        # finalization
        self.__v2 ^= 0xff
        for i in range(self.__d):
            self.__SipRound()
        return self.__v0 ^ self.__v1 ^ self.__v2 ^ self.__v3

    def hashId(self, text):
        """
        :category: Python function
        :rubric: PY
        :example: hashId("youpi") >>>(5107726104778734155)
        :dsc:
            Produce a unique ID for a given string. This can be used in a datamodel to replace the internal numbers.
        :return: The hashId
        :link Documentation: https://github.com/bozhu/siphash-python
        """
        return self.auth(0x0f0e0d0c0b0a09080706050403020100, text)

if __name__ == '__main__':
    my_siphash = SipHash()

    k = 0x0f0e0d0c0b0a09080706050403020100
    # m = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e'
    # m = '\x00\x01\x02\x03\x04\x05\x06\x07'
    # print hex(my_siphash.auth(k, m))

    test_vectors = [
        0x726fdb47dd0e0e31, 0x74f839c593dc67fd, 0x0d6c8009d9a94f5a,
        0x85676696d7fb7e2d, 0xcf2794e0277187b7, 0x18765564cd99a68d,
        0xcbc9466e58fee3ce, 0xab0200f58b01d137, 0x93f5f5799a932462,
        0x9e0082df0ba9e4b0, 0x7a5dbbc594ddb9f3, 0xf4b32f46226bada7,
        0x751e8fbc860ee5fb, 0x14ea5627c0843d90, 0xf723ca908e7af2ee,
        0xa129ca6149be45e5, 0x3f2acc7f57c29bdb, 0x699ae9f52cbe4794,
        0x4bc1b3f0968dd39c, 0xbb6dc91da77961bd, 0xbed65cf21aa2ee98,
        0xd0f2cbb02e3b67c7, 0x93536795e3a33e88, 0xa80c038ccd5ccec8,
        0xb8ad50c6f649af94, 0xbce192de8a85b8ea, 0x17d835b85bbb15f3,
        0x2f2e6163076bcfad, 0xde4daaaca71dc9a5, 0xa6a2506687956571,
        0xad87a3535c49ef28, 0x32d892fad841c342, 0x7127512f72f27cce,
        0xa7f32346f95978e3, 0x12e0b01abb051238, 0x15e034d40fa197ae,
        0x314dffbe0815a3b4, 0x027990f029623981, 0xcadcd4e59ef40c4d,
        0x9abfd8766a33735c, 0x0e3ea96b5304a7d0, 0xad0c42d6fc585992,
        0x187306c89bc215a9, 0xd4a60abcf3792b95, 0xf935451de4f21df2,
        0xa9538f0419755787, 0xdb9acddff56ca510, 0xd06c98cd5c0975eb,
        0xe612a3cb9ecba951, 0xc766e62cfcadaf96, 0xee64435a9752fe72,
        0xa192d576b245165a, 0x0a8787bf8ecb74b2, 0x81b3e73d20b49b6f,
        0x7fa8220ba3b2ecea, 0x245731c13ca42499, 0xb78dbfaf3a8d83bd,
        0xea1ad565322a1a0b, 0x60e61c23a3795013, 0x6606d7e446282b93,
        0x6ca4ecb15c5f91e1, 0x9f626da15c9625f3, 0xe51b38608ef25f57,
        0x958a324ceb064572
    ]

    m = ''
    for i in range(len(test_vectors)):
        assert my_siphash.auth(k, m) == test_vectors[i]
        m += chr(i)
    print('all test vectors passed')
