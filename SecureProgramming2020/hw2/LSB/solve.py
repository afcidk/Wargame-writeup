from pwn import *
from Crypto.Util.number import *

r = remote('140.112.31.97', 30001)

n = int(r.recvline().split(b' = ')[1])
c = int(r.recvline().split(b' = ')[1])
e = 65537
print(n, c)

_3e = pow(3, e, n)

L, R = 0, n
while L != R:
    c = (c * _3e) % n
    r.sendline(str(c))
    m = int(r.recvline().split(b' = ')[1])
    intv = (R - L - 1) // 3
    if m == 0:
        R = L + intv - 1
    elif m == (-n) % 3:
        L = L + intv
        R = R - intv - 1
    elif m == (-2 * n) % 3:
        L = R - intv

# The answer is unstable. So I bruteforced all plaintext near the computed value
# FLAG{nF9Px2LtlNh5fJiq3QtG}
for i in range(L - 200, L + 200):
    plaintext = long_to_bytes(i)
    print(long_to_bytes(i))
