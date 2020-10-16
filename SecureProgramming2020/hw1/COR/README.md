# COR
Three chained LFSR pseudo-random number generator. We could apply correlation attack to it. Calculate the probability of each LFSR output with the result (`(x1 & x2) ^ ((not x1) & x3)`), and bruteforce the initial state to complete the challenge.

Script to solve this challenge is located at [bruteforce.py](./bruteforce.py)
