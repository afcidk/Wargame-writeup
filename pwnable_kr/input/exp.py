import subprocess
import socket
import os
import time
import random

port = random.randint(10000, 20000)
argv = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "", " \n\r", str(port), "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"]

stdinr, stdinw = os.pipe()
stderrr, stderrw = os.pipe()

os.write(stdinw, b'\x00\x0a\x00\xff')
os.write(stderrw, b'\x00\x0a\x02\xff')
os.putenv(b'\xde\xad\xbe\xef', b'\xca\xfe\xba\xbe')

with open('\n', 'w') as f:
    f.write('\x00')
    f.write('\x00')
    f.write('\x00')
    f.write('\x00')

pipe = subprocess.Popen(['./input'] + argv, stdin=stdinr, stderr=stderrr)

time.sleep(2) # Wait for socket to establish
# TODO: /bin/cat flag but we are at /tmp?
s = socket.socket()
s.connect(('127.0.0.1', port))
s.send(b'\xde\xad\xbe\xef')
s.close()
