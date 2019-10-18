from pwn import *

argv = ['\x01' for i in range(2018)]
env = {'\x01':'hi'}
print(argv, env)
r = process(executable='2018.rev', argv=argv, env=env)

r.interactive()
