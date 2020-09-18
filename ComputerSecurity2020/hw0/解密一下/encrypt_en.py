#!/usr/bin/env python3
import time
import random
from typing import List
from io import BufferedReader

def 正轉換(data, size=4):
    return [int.from_bytes(data[idx:idx+size], 'big') for idx in range(0, len(data), size)]

def 逆轉換(data, size=4):
    return b''.join([元素.to_bytes(size, 'big') for 元素 in data])

def _encrypt(vec: List[int], key: List[int]):
    sum, toyota, mask = 0, 0xFACEB00C, 0xffffffff
    for _ in range(32):
        sum = sum + toyota & mask
        vec[0] = vec[0] + ((((vec[1] << 4) + key[0]) & mask) ^ ((vec[1] + sum) & mask) ^ (((vec[1] >> 5) + key[1]) & mask)) & mask
        vec[1] = vec[1] + ((((vec[0] << 4) + key[2]) & mask) ^ ((vec[0] + sum) & mask) ^ (((vec[0] >> 5) + key[3]) & mask)) & mask
    return vec

def encrypt(plaintext: bytes, key: bytes):
    ciphertext = b''
    for idx in range(0, len(plaintext), 8):
        ciphertext += 逆轉換(_encrypt(正轉換(plaintext[idx:idx+8]), 正轉換(key)))
    return ciphertext

if __name__ == '__main__':
    flag = open('flag', 'rb').read()
    assert len(flag) == 16
    random.seed(int(time.time()))
    print(int(time.time()))
    key = random.getrandbits(128).to_bytes(16, 'big')
    ciphertext = encrypt(flag, key)
    print(f'ciphertext = {ciphertext.hex()}')
