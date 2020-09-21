#!/usr/bin/env python3
import time
import random
from typing import List


def positive(data, size=4):
    return [
        int.from_bytes(data[idx:idx + size], 'big')
        for idx in range(0, len(data), size)
    ]


def negative(data, size=4):
    return b''.join([ele.to_bytes(size, 'big') for ele in data])


def _decrypt(vec: List[int], key: List[int]):
    toyota, mask = 0xFACEB00C, 0xffffffff
    for i in range(32, 0, -1):
        sum = 0
        for t in range(i):
            sum = sum + toyota & mask
        prev0 = ((((vec[0] << 4) + key[2]) & mask) ^ ((vec[0] + sum) & mask) ^
                 (((vec[0] >> 5) + key[3]) & mask))
        vec[1] = (vec[1] - prev0) & mask
        prev1 = ((((vec[1] << 4) + key[0]) & mask) ^ ((vec[1] + sum) & mask) ^
                 (((vec[1] >> 5) + key[1]) & mask))
        vec[0] = (vec[0] - prev1) & mask
    return vec


def decrypt(ciphertext: bytes, key: bytes):
    plaintext = b''
    for idx in range(0, len(ciphertext), 8):
        plaintext += negative(
            _decrypt(positive(ciphertext[idx:idx + 8]), positive(key)))
    return plaintext


# Solution: 1599977586 b'FLAG{4lq7mWGh93}'
if __name__ == '__main__':
    # This ciphertext is copied manually from output.txt
    ciphertext = b'\x77\xf9\x05\xc3\x9e\x36\xb5\xeb' \
                 b'\x0d\xee\xcb\xb4\xeb\x08\xe8\xcb'

    # Test all seeds till found a decrypted text with FLAG prefix
    cur = int(time.time())
    while True:
        random.seed(cur)
        key = random.getrandbits(128).to_bytes(16, 'big')
        plaintext = decrypt(ciphertext, key)
        print(cur, plaintext)
        if plaintext[:4] == b"FLAG": break
        cur -= 1
