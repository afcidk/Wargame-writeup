#!/usr/bin/env python3
from functools import reduce
from string import printable
from itertools import combinations


# Shamelessly copy from generate.py Q_Q
class LFSR:
    def __init__(self, init, feedback):
        self.state = init
        self.feedback = feedback

    def getbit(self):
        nextbit = reduce(lambda x, y: x ^ y,
                         [i & j for i, j in zip(self.state, self.feedback)])
        self.state = self.state[1:] + [nextbit]
        return nextbit


class MYLFSR:
    def __init__(self, inits):
        inits = [[int(i) for i in f"{int.from_bytes(init, 'big'):016b}"]
                 for init in inits]
        self.l1 = LFSR(inits[0], [int(i) for i in f'{39989:016b}'])
        self.l2 = LFSR(inits[1], [int(i) for i in f'{40111:016b}'])
        self.l3 = LFSR(inits[2], [int(i) for i in f'{52453:016b}'])

    def getbit(self):
        x1 = self.l1.getbit()
        x2 = self.l2.getbit()
        x3 = self.l3.getbit()
        return (x1 & x2) ^ ((not x1) & x3)


def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])


def cmp_cnt(a, b):
    cnt = 0
    for x, y in zip(a, b):
        if x == y: cnt += 1
    return cnt


output = [
    1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0,
    1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
    1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1
]
# Idea: Bruteforce flag[4:6], flag[2:4] and compare the LFSR getbit output with output
# After that, use MYLFSR to bruteforce all possible candidates and find which candidate
# generates the same output

# Get flag[4:6] candidates
candidates = [[], [], []]
cnt_list = {}
for a in printable:
    for b in printable:
        n = (a + b).encode()
        lfsr = LFSR([int(i) for i in f"{int.from_bytes(n, 'big'):016b}"],
                    [int(i) for i in f'{52453:016b}'])
        cnt = cmp_cnt([lfsr.getbit() for _ in range(100)], output)
        if cnt not in cnt_list:
            cnt_list[cnt] = [n]
        else:
            cnt_list[cnt].append(n)

keys = sorted(cnt_list)
for i in range(1, 4):  # 1~3
    for e in cnt_list[keys[-i]]:
        candidates[2].append(e)

# Get flag[2:4] candidates
cnt_list = {}
for a in printable:
    for b in printable:
        n = (a + b).encode()
        lfsr = LFSR([int(i) for i in f"{int.from_bytes(n, 'big'):016b}"],
                    [int(i) for i in f'{40111:016b}'])
        cnt = cmp_cnt([lfsr.getbit() for _ in range(100)], output)
        if cnt not in cnt_list:
            cnt_list[cnt] = [n]
        else:
            cnt_list[cnt].append(n)

keys = sorted(cnt_list)
for i in range(1, 4):  # 1~3
    for e in cnt_list[keys[-i]]:
        candidates[1].append(e)
print(candidates)

for c1 in candidates[1]:
    for c2 in candidates[2]:
        for a in printable:
            for b in printable:
                n = (a + b).encode()
                lfsr = MYLFSR([n, c1, c2])
                if [lfsr.getbit() for _ in range(100)] == output:
                    print(
                        f"flag: FLAG{{{n.decode()}{c1.decode()}{c2.decode()}}}"
                    )
