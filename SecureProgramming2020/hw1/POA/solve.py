#!/usr/bin/env python3
from pwn import *
from binascii import hexlify
from string import printable

#r = process('./server.py')
r = remote('140.112.31.97', 30000)
r.recvuntil(' = ')
cipher = bytes.fromhex(r.recvline()[:-1].decode())
flag = ''
modified = ''
print(hexlify(cipher))

# Idea: Find the padding head (0x80) first, then modify the end of cipher to [0x80, 0x00] and move forward

# Find padding head by testing bytes by xoring 0x80
# (If that byte is already 0x80, 0x80^0x80 = 0, the unpad check would report failure)
head = len(cipher) - 17
while True:
    cur = cipher[:head] + bytes([cipher[head] ^ 0x80]) + cipher[head + 1:]
    r.sendlineafter(' = ', hexlify(cur))
    if r.recvline()[:-1] == b'YESSSSSSSS':
        head -= 1
    else:
        break
print('head index: ' + str(head))

# Bruteforce backword byte by byte, make sure to make the last two bytes [0x80, 0x00]
modified = bytes([cipher[head] ^ 0x80]) + cipher[head + 1:len(cipher) - 16]
head -= 1
while True:  # Bruteforce all blocks
    for _ in range(16):  # Bruteforce one block
        for i in range(0xff + 1):  # Bruteforce one byte
            cur = cipher[:head] + bytes([i]) + modified + cipher[-16:]
            r.sendlineafter(' = ', hexlify(cur))
            if r.recvline()[:-1] == b'YESSSSSSSS':
                flag_byte = i ^ 0x80 ^ cipher[head]
                modified = bytes([cipher[head] ^ flag_byte ^ 0x00]) + modified
                flag = chr(flag_byte) + flag
                print('-->', flag)
                head -= 1
                break
    cipher = cipher[:-16]
    if len(cipher) == 16: break  # Exit if remains only one block
    modified = ''
    head = len(cipher) - 17

# Flag: FLAG{31a7f10f1317f622}
