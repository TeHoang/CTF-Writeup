#!/usr/local/bin/python
from Crypto.Util.number import *
from pwn import *

io = remote('be.ax', 31102)
n = int(io.recvline().decode().strip('n = '))
e = int(io.recvline().decode().strip('e = '))
ct = int(io.recvline().decode().strip('ct = '))

three = pow(3, e, n)

def base(x):
    out = ""
    while x:
        out = str(x % 3) + out
        x //= 3
    return out

def check(guess):
    if len(guess) == len(base(n)):
        return False
    else:
        return True

guess = ""
while check(guess):
    print(guess)
    mult = pow(three, len(guess) + 1, n)
    io.sendline(str(mult % n).encode())
    res = io.recvline().strip().decode()
    if "Fizz" in res:
        guess += "0"
        continue
    mult = -mult % n
    io.sendline(str(mult % n).encode())
    res = io.recvline().strip().decode()
    if "Fizz" in res:
        guess += "2"
        continue
    guess += "1"

a = (int(guess, 3) * n) // (3 ** len(guess))
guess = ""

ct *= pow(a+1, -e, n)

while check(guess):
    print(guess)
    mult = pow(three, len(guess) + 1, n)
    io.sendline(str(ct * mult % n).encode())
    res = io.recvline().strip().decode()
    if "Fizz" in res:
        guess += "0"
        continue
    mult = -mult % n
    io.sendline(str(ct * mult % n).encode())
    res = io.recvline().strip().decode()
    if "Fizz" in res:
        guess += "2"
        continue
    guess += "1"

print(long_to_bytes((int(guess, 3) * n) // (3 ** len(guess))))

# x < n/3 -> Fizz
# n/3 < x < 2n/3 -> -n % 3
# 2n/3 < x < n -> n % 3 -> -3n will Fizz