from z3 import *

def isPrime(x):
    y, z = BitVecs('y z', 33)
    # Added y==x/z to prevent overflow case
    return And(x>1, Not(Exists([y, z], And(y<x,z<x,y>1,z>1,x==y*z, y==x/z))))

s = Solver()

# Since the number could be unsigned int, I use 33 bit vector :b
a1, a2 = BitVecs('a1 a2', 33)
c1 = BitVecVal(-574406350, 33)
c2 = BitVecVal(1931514558, 33)
c3 = BitVecVal(3295, 33)

s.add(a1*a2 == c1)
s.add((a1^0x7e)*(a2+16) == c2)
s.add((((a1&0xffff)-(a2&0xffff))&0xfff) == 3295)
s.add(isPrime(a1))

while s.check() == sat:
    print(f"{s.model()[a1]}-{s.model()[a2]}")
    s.add(Or(a1 != s.model()[a1], a2 != s.model()[a2]))
