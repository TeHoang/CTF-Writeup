---
title: "Zer0ptsCTF2023"
date: 2023-07-18T18:08:47+07:00
draft: false
tags:
    - crypto
    - ctf 
    - writeup
---

# easy_factoring
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     102   |     95    |

## Description
```text
The word "decomposition" has multiple meanings.
Can you decompose?
```
## Challenge's script
```python
import os
import signal
from Crypto.Util.number import *

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

def main():
    p = getPrime(128)
    q = getPrime(128)
    n = p * q

    N = pow(p, 2) + pow(q, 2)

    print("Let's factoring !")
    print("N:", N)

    p = int(input("p: "))
    q = int(input("q: "))

    if isPrime(p) and isPrime(q) and n == p * q:
        print("yey!")
        print("Here you are")
        print(flag)
    else:
        print("omg")

def timeout(signum, frame):
    print("Timed out...")
    signal.alarm(0)
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    main()
    signal.alarm(0)
```
## Solution

//Explanation later

```python
from Crypto.Util.number import isPrime
from sage.all import *
from pwn import *

def solve():
    flag = False 
    while not flag:
        with remote('crypto.2023.zer0pts.com', 10333, level = 'debug') as r:
            r.recvuntil("N: ")
            N = int(r.recvline().strip())
            a = two_squares(N)
            p, q = int(a[0]), int(a[1])
            if isPrime(p) and isPrime(q) and pow(p, 2) + pow(q, 2) == N:
                r.sendline(''.join(map(str,str(p))).encode())
                r.sendline(''.join(map(str,str(q))).encode())
                print(r.recvuntil(b'}').decode())
                flag = true
            else:
                continue

solve()

# zer0pts{piyopiyo_Fermat's_Sum_of_Square_meow!!}
```

# SquareRNG
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto, warmup  |     130   |     54    |

## Description
```text
I wrote a pseudorandom number generator. You can't guess the next bit without knowing each other's secret.
```

## Challenge's script

```python
#!/usr/bin/env python3
import os
from Crypto.Util.number import getPrime, getRandomRange

def isSquare(a, p):
    return pow(a, (p-1)//2, p) != p-1

class SquareRNG(object):
    def __init__(self, p, sa, sb):
        assert sa != 0 and sb != 0
        (self.p, self.sa, self.sb) = (p, sa, sb)
        self.x = 0

    def int(self, nbits):
        v, s = 0, 1
        for _ in range(nbits):
            self.x = (self.x + 1) % p
            s += pow(self.sa, self.x, self.p) * pow(self.sb, self.x, self.p)
            s %= self.p
            v = (v << 1) | int(isSquare(s, self.p))
        return v

    def bool(self):
        self.x = (self.x + 1) % self.p
        t = (pow(self.sa, self.x, self.p) + pow(self.sb, self.x, self.p))
        t %= self.p
        return isSquare(t, self.p)

p = getPrime(256)

sb1 = int(input("Bob's seed 1: ")) % p
sb2 = int(input("Bob's seed 2: ")) % p
for _ in range(77):
    sa = getRandomRange(1, p)
    r1 = SquareRNG(p, sa, sb1)
    print("Random 1:", hex(r1.int(32)))
    r2 = SquareRNG(p, sa, sb2)
    print("Random 2:", hex(r2.int(32)))

    guess = int(input("Guess next bool [0 or 1]: "))
    if guess == int(r1.bool()):
        print("OK!")
    else:
        print("NG...")
        break
else:
    print("Congratz!")
    print(os.getenv("FLAG", "nek0pts{*** REDACTED ***}"))
```

## Solution
```python
from Crypto.Util.number import *
from pwn import * 

host, port = 'crypto.2023.zer0pts.com', 10666

def solve():
    with remote(host, port, level = 'debug') as r:
        r.recvuntil("Bob's seed 1:")
        r.sendline(''.join(map(str,str(1))).encode())
        r.recvuntil("Bob's seed 2:")
        r.sendline(''.join(map(str,str(-1))).encode())
        for i in range(77):
            r.recvuntil("Random 1:")
            r1 = int(r.recvuntil(b'\n').strip(), 16)
            r.recvuntil("Random 2:")
            r2 = int(r.recvuntil(b'\n').strip(), 16)
            r1, r2 = str(bin(r1)[2:]), str(bin(r2)[2:])
            print(len(r1), len(r2))
            # print(r1.bit_count(), r2.bit_count())
            if len(r1) == 32: #r1[0] = 1
                print(1, r2[-1])
                if r2[-1] == '1':
                    r.sendline(''.join(map(str,str(1))).encode())
                else:
                    r.sendline(''.join(map(str,str(0))).encode())
            else: #r1[0] = 0
                print(0, r2[-1])
                if r2[-1] == '1':
                    r.sendline(''.join(map(str,str(0))).encode())
                else:
                    r.sendline(''.join(map(str,str(1))).encode())
            r.recvline()    


solve()

# zer0pts{L(a)L(b)=L(ab)}
```
