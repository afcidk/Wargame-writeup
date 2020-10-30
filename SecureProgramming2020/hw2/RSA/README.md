## RSA
In this challenge we are given two files, namely `generate.py` and `output.txt`. `generate.py` contains the algorithm to encrypt the flag, and the output is placed in `output.txt`.

We can take a look at `generate.py` first.
```python=
#!/usr/bin/env python3
import random
from Crypto.Util.number import *
from gmpy2 import next_prime

def pad(data, block_size):
    padlen = block_size - len(data) - 2
    if padlen < 8:
        raise ValueError
    return b'\x00' + bytes([random.randint(1, 255) for _ in range(padlen)]) + b'\x00' + data

FLAG = open('./flag', 'rb').read()

p = getPrime(512)
q1 = next_prime(2 * p)
q2 = next_prime(3 * q1)

n = p * q1 * q2
e = 65537

m = bytes_to_long(pad(FLAG, 192))
c = pow(m, e, n)
print(f'n = {n}')
print(f'c = {c}')
```

The encryption method is RSA. Unlike the classic RSA encryption method, this algorithm takes three input (`p`, `q1`, `q2`), and use them to calculate N.

However, that's not the case, since RSA algorithm can handle multiple prime as well (reference: https://crypto.stackexchange.com/questions/11287/rsa-with-modulus-product-of-many-primes). The fallback of multiple prime might be in the weakness of small primes. In this challenge we can verify that the three primes are all larger than 512 bits, so it seems impossible to bruteforce all possible p, q1 and q2 **individually**.

One more thing I've noticed is that p, q1, and q2 seem to have some relationship. What if I only bruteforce `p`, and calculate the corresponding `q1` and `q2`? In this way the bruteforce times would decrease from $2^{512} \times 2^{512} \times 2^{512}$ to only $2^{512}$. Looks good!

$2^{512}$ is still too big. We only have one variable now, maybe we can try to use binary search to find the correct p by comparing the calculated n and the real n.

The script to solve this challenge is located at [solve.py](./solve.py)
