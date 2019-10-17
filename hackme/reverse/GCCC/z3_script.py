#!/usr/bin/env python3
from z3 import *

# The array from binary file
array = [164, 25, 4, 130, 126, 158, 91, 199, 173, 252, 239, 143, 150, 251, 126, 39, 104, 104, 146, 208, 249, 9, 219, 208, 101, 182, 62, 92, 6, 27, 5, 46]

array = [BitVecVal(i, 40) for i in array] # BitVecVal means a **fixed value** with BitVec type
b = [BitVec('b{}'.format(i), 40) for i in range(33)]
result = BitVec('result', 40) # Int() does not support bitwise operation
text = [Int('flag{}'.format(i)) for i in range(40)]
solver = Solver()
solver.set(unsat_core=True) 

# Set up known restrictions
solver.assert_and_track(text[0] == ord("F"), "F")
solver.assert_and_track(text[1] == ord("L"), "L")
solver.assert_and_track(text[2] == ord("A"),"A")
solver.assert_and_track(text[3] == ord("G"),"G")
solver.assert_and_track(text[4] == ord("{"),"{")
solver.assert_and_track(text[31] == ord("}"),"}")
solver.assert_and_track(b[0] == 0, "xored_b0")

for i in range(32):
    if i >= 5 and i <= 30:
        solver.add(Or(text[i] == ord(' '), And(text[i] >= ord('A'), text[i] <= ord('Z'))))
    solver.assert_and_track(b[i+1] == b[i]^array[i]&0xff, 'xored_b{}'.format(i+1))

    solver.assert_and_track(text[i] == BV2Int(array[i]^((result>>i)&0xff)^b[i]), 'main{}'.format(i))

if solver.check() == sat:
    m = solver.model()
    s = ''.join(chr(m[text[i]].as_long()) for i in range(32))
    print(s)
else:
    print(solver.unsat_core())
