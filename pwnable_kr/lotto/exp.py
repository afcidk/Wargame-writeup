import subprocess
import os

p = subprocess.Popen('./lotto', stdin=subprocess.PIPE, stdout=subprocess.PIPE)

print(p.stdout)

