from Crypto.Util.number import *

with open('out.txt') as f:
    p = int(f.readline())
    line = f.readline().strip()[1:-1]
    L = [int(l) for l in line.split(',')]

flag = (L[6] - L[5] - L[2] + L[1] - L[4] + L[3] + L[0]) % p

print(long_to_bytes(flag))

# corctf{mind your ones and zeroes because zero squared is zero and one squared is one}