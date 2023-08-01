---
title: "CorCTF"
date: 2023-08-01T18:35:46+07:00
draft: false
tags:
    - crypto
    - ctf 
    - writeup
ToC: true
---

Tiếp tục trên hành trình feed giải 

# fizzbuzz100
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     121   |     134    |

## Description
```
lsb oracles are pretty overdone... anyway here's fizzbuzz
```
## Challenge
```python
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

while True:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    if not out:
        out = pt
    print(out)
```

Đề cho mình gửi $ct$ đến server và tính $ct^d \pmod{n}$, nếu $pt = flag$ thì sẽ disconnect còn nếu như $pt \equiv 0 \pmod{3}$ thì ta có out = "Fizz", $pt \equiv 0 \pmod{5}$ thì có out = "Buzz", $pt \equiv 0 \pmod{15}$ thì sẽ có "FizzBuzz". Nếu như $(pt, 15) = 1$ thì ta sẽ có được $pt$

## Solution
Gửi cho server $(r^e*ct)\pmod{n}$ sao cho $(r, 15)=1$, lúc này ta sẽ có được $pt = (r^e*ct)^d \equiv (r*flag) \pmod{n}$. Nhân $r^{-1}$ vào $pt$ thì ta sẽ có được $flag$

```python
from Crypto.Util.number import long_to_bytes as ltb
from pwn import * 

def solve():
    with remote('be.ax', 31100) as r:
        n = int(r.recvline().decode().strip('n = '))
        e = int(r.recvline().decode().strip('e = '))
        ct = int(r.recvline().decode().strip('ct = '))
        r.sendlineafter('>',str((pow(2, e, n) * ct) % n))
        pt = int(r.recvline().decode().strip('pt = '))
        print(ltb((pow(2, -1, n) * pt) % n))

solve()

# corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}
```

# eyes
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     140   |     75    |

## Description
```
can you see it?
```

## Challenge

```python
from Crypto.Util.number import bytes_to_long, getPrime

# my NEW and IMPROVED secret sharing scheme!! (now with multivariate quadratics)

with open('flag.txt', 'rb') as f:
    flag = f.read()

s = bytes_to_long(flag)
p = getPrime(len(bin(s)))
print(p)
F = GF(p)
N = 1024

conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])

A = random_matrix(F, N, N)

for i in range(0, N):
    for j in range(0, i):
        A[i, j] = 0
B = random_matrix(F, N, 1)
C = matrix(F, [F(s)])

fn = lambda x: (x.T * A * x + B.T * x + C)[0][0]

L = []
for i in range(7):
    L.append(fn(conv(i + 1)))

print(L)
```

## Solution
Note:
```math
$$
\begin{aligned}
A &= 
\left(\begin{array}{cc} 

a_{0,0} & a_{0,1}   &  \dots & a_{0,N-1}          \\
0       & a_{1, 1}  &  \dots & a_{1,N-1}         \\
\vdots  & \ddots    &        & \vdots        \\
0       & \dots     &  0     & a_{N-1, N-1}
\end{array}\right) \\
\\
B &= \left(\begin{array}{cc} 
b_0   \\
b_1      \\
\vdots     \\
b_{N-1}     
\end{array}\right) 
\\ \\
C &= flag
\end{aligned}
$$
```
Sau một hồi quan sát code và nháp thì chúng ta sẽ có các đẳng thức sau:
$$
\begin{aligned}
L_0 &= a_{0,0} + b_0 + flag \\
L_1 &= a_{1, 1} + b_1 + flag \\
L_2 &= a_{0, 0} + a_{0,1} + a_{1,1} + b_0 + b_1 + flag \\
L_3 &= a_{2,2} + b_2 + flag \\
L_4 &= a_{0,0} + a_{0,2} + a_{2,2} + b_0 + b_2 + flag \\
L_5 &= a_{1,1} + a_{1,2} + a_{2,2} + b_1 + b_2 + flag \\
L_6 &= a_{0,0} + a_{0,1} + a_{0,2} + a_{1,1} + a_{1,2} + a_{2,2} + b_0 + b_1 + b_2 + flag

\end{aligned}
$$

Ta thu được $flag$ bằng $L_0 + L_1 + L_3 + L_6 - L_2 - L_4 - L_5$

```python
from Crypto.Util.number import *

with open('out.txt') as f:
    p = int(f.readline())
    line = f.readline().strip()[1:-1]
    L = [int(l) for l in line.split(',')]

flag = (L[6] - L[5] - L[2] + L[1] - L[4] + L[3] + L[0]) % p

print(long_to_bytes(flag))

# corctf{mind your ones and zeroes because zero squared is zero and one squared is one}
```

# cbc
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     152   |     59    |

## Description
```
who on earth is putting CLASSICAL BORING CRYPTOGRAPHY in my ctf
```

## Challenge

```python
import random

def random_alphastring(size):
    return "".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i+klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext
    
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

message = open("message.txt").read().upper()
message = "".join([char for char in message if char in alphabet])
flag = open("flag.txt").read()
flag = flag.lstrip("corctf{").rstrip("}")
message += flag
assert all([char in alphabet for char in message])

key = random_alphastring(bs)
iv, ct = cbc(key, pad(bs, message))
print(f"{iv = }")
print(f"{ct = }")
```
Note: $ \{A, B, \dots, Z \}= \{0, 1, \dots, 25\}$ 


Đặt $a_i$ là các kí tự của flag và $c_i$ là các kí tự của ciphertext

Ta có:

$$
\begin{aligned}
c_1 &\equiv iv_1 + a_1 + k_1    &\pmod{26} \\
c_2 &\equiv iv_2 + a_2 + k_2    &\pmod{26} \\
\vdots                      \\
c_{16} &\equiv iv_{16} + a_{16} + k_{16}&\pmod{26} \\
c_{17} &\equiv c_1 + a_{17} + k_1       &\pmod{26} \\
\vdots                              \\
c_n &\equiv c_{n - 16} + a_n + k_{(n \% 16) + 1} &\pmod{26}
\end{aligned}
$$

Cần tìm các $a_i$

## Solution

Ta chuyển thành $c'_i \equiv a_i + k_i \pmod{26}$ để giống như vigenere-cipher sau đó quăng lên [dcode](https://www.dcode.fr/vigenere-cipher) để decode...

```python
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

with open('cbc_output.txt') as f:
    iv = f.readline().strip().split('iv = ')[-1][1:-1]
    ct = f.readline().strip().split('ct = ')[-1][1:-1]

ct = [char for char in ct]
iv = [char for char in iv]

for i in range(len(ct) - 1, 15, -1):
    ct[i] = alphabet[(alphabet.index(ct[i]) - alphabet.index(ct[i - 16]))]

for i in range(0, 16):
    ct[i] = alphabet[(alphabet.index(ct[i]) - alphabet.index(iv[i]))]

ct = "".join(char for char in ct)
print(ct[-16 * 10:]) # Decode this

# corctf{ATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS}

```

# fizzbuzz101
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     251   |     19    |

## Description
```
'but in real fizzbuzz you say the number' - someone, probably
```

## Challenge
```python
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

while True:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    if not out:
        out = "101"
    print(out)
```

Phần tiếp theo của fizzbuzz100, bây giờ đề sẽ không trả về $pt$ cho chúng ta nữa mà chỉ trả về "101", điều này có nghĩa là ta sẽ không thể lấy lại được $flag$. Sike, just kidding, đây là một bài [LSB Oracle](https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack) nhưng thay vì xét mod 2 thì chúng ta sẽ xét mod 3. Lần đầu tiên mình gặp dạng bài này nên đã ăn hành và chỉ có thể cố gắng xem hint và upsolve sau contest :(

## Solution

Mình sẽ đặt m là flag để tiện, chúng ta sẽ phân tích ba trường hợp khi chúng ta gửi $(ct * 3^e)$ (thực ra là hai và loại trừ ra trường hợp còn lại):

Khi này server sẽ decrypt và tính ra $ pt = 3*m$

* Trường hợp đầu tiên:  $m < \dfrac{n}{3}$

Từ đây

$$\begin{aligned} 
&\Rightarrow 3m < n \\
&\Rightarrow 3m \equiv 3m \pmod{n} \\ 
&\Rightarrow 3m \equiv 0 \pmod{3} 
\end{aligned}
$$

Vậy ta sẽ nhận được "Fizz"

* Trường hợp thứ hai: $ \dfrac{2n}{3} < m < n$

Để ý rằng $n - m < n - \dfrac{2n}{3} = \dfrac{n}{3}$

$$\begin{aligned} 
&\Rightarrow 3(n - m) < n \\
&\Rightarrow 3(n - m) \equiv -3m \pmod{n} \\ 
&\Rightarrow -3m \equiv 0 \pmod{3} 
\end{aligned}
$$

Và ta cũng sẽ nhận được "Fizz"

Vậy ta có thể tóm tắt lại như sau:

Gửi $(ct * 3^e)$: 
* Nếu ta nhận được "Fizz" $\Rightarrow m \in (0, \dfrac{n}{3}) $
* Nếu không, ta sẽ gửi $(ct * -3 ^ e)$ để server sẽ tính ra $pt \equiv -3m \pmod{n}$. Lúc này nếu ta nhận được "Fizz" $\Rightarrow m \in (\dfrac{2n}{3}, n)$
* Không thì $m \in (\dfrac{n}{3}, \dfrac{2n}{3}) $

Bằng cách này ta đã có thể rút ngắn được khoảng m ban đầu từ $m \in (0, n)$ xuống còn 1 trong 3 khoảng trên. Chúng ta sẽ thực hiện tiếp quá trình này để khoảng này hẹp nhất có thể và tìm ra $m$

```python
from pwn import *
from Crypto.Util.number import * 

def solve():
    def len_base3(n):
        res = 0 
        while n:
            res += 1
            n //= 3
        return res 
    
    with remote("be.ax", 31101) as r:
        n = int(r.recvline().decode().strip('n = '))
        e = int(r.recvline().decode().strip('e = '))
        ct = int(r.recvline().decode().strip('ct = '))
        s = ""
        for k in range(1, len_base3(n) + 1):
            print(s)
            m = pow(pow(3, e, n), k, n)
            to_send = (ct * m) % n
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv:
                s += "0"
                continue 
            to_send = (ct * -m) % n
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv: 
                s += "2" 
            else: 
                s += "1"
        print(long_to_bytes((int(s, 3) * n) // (3 ** len(s))))

solve()

# corctf{''.join(fizz_buzz(x) for x in range(99, 102)) == "FizzBuzz101" == cool_username}
```

# fizzbuzz102
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     290   |     14    |

## Description
```
did you really think i wasn't going to add an lcg challenge somewhere
```
## Challenge

```python
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom
from secrets import randbits

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

a = randbits(845)
b = randbits(845)
def lcg(x):
    return (a * x + b) % n

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

while True:
    ct = int(input("> "))
    pt = lcg(pow(ct, d, n))
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    if not out:
        out = "101"
    print(out)
```

Phần tiếp theo của fizzbuzz101, thay vì tính $pt \equiv ct^d \pmod{n}$ thì giờ đề bài sẽ tính $pt \equiv a*ct^d + b \pmod{n}$ 

## Solution
Chúng ta hoàn toàn có thể áp dụng kỹ thuật như fizzbuzz101 để tìm $a$, sau đó ta chỉ cần nhân $a^{-e}$ vào $ct$

```python
from pwn import *
from Crypto.Util.number import * 

def solve():
    def len_base3(n):
        res = 0 
        while n:
            res += 1
            n //= 3
        return res 

    with remote("be.ax", 31102) as r:
        n = int(r.recvline().decode().strip('n = '))
        e = int(r.recvline().decode().strip('e = '))
        ct = int(r.recvline().decode().strip('ct = '))
        s = ""
        for k in range(1, len_base3(n) + 1):
            print(s)
            m = pow(pow(3, e, n), k, n)
            to_send = m
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv:
                s += "0"
                continue 
            to_send = -m % n
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv: 
                s += "2" 
            else: 
                s += "1"
        
        a = int(s, 3) * n // (3 ** len(s))
        print("a OK")
        ct *= pow(a + 1, -e, n) #huh...

        s = ""
        for k in range(1, len_base3(n) + 1):
            print(s)
            m = pow(pow(3, e, n), k, n)
            to_send = (ct * m) % n
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv:
                s += "0"
                continue 
            to_send = (ct * -m) % n
            r.sendline(str(to_send).encode())
            recv = r.recvline().decode().strip()
            if "Fizz" in recv: 
                s += "2" 
            else: 
                s += "1"
        print(long_to_bytes((int(s, 3) * n) // (3 ** len(s))))

solve()

# corctf{fizzbuzz_1s_4_r4th3r_s1lly_f0rm_0f_l34k4g3_d0nt_y0u_th1nk?n0w_w1th_4dd3d_LCG_f0r_fun!}
```

# QCG-k
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     272   |     16    |

## Description
```
The Q stands for quintadecic (obviously)
```

## Challenge
```python
from random import randint
from Crypto.Util.number import inverse, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha256
import os

class PRNG:
    def __init__(self, mod):
        self.coeffs = [randint(1,mod) for _ in range(16)]
        self.mod = mod
        self.state = randint(1, mod)
    def next(self):
        self.state = sum(coeff * self.state**i for i,coeff in enumerate(self.coeffs)) % self.mod
        return self.state

q = 77897050769654696452572824710099972349639759246855689360228775736949644730457
p = ...
g = ...

x = randint(1, q - 1)
y = pow(g,x,p)

kPRNG = PRNG(q)

def hsh(msg):
    return bytes_to_long(sha256(msg).digest())

def sign(msg):
    k = kPRNG.next()
    r = pow(g,k,p) % q
    s = (inverse(k, q) * (hsh(msg) + x*r)) % q
    if r == 0 or s == 0:
        return sign(msg)
    return r,s

with open("quotes.txt") as f:
    for quote in f:
        quote = quote.strip().encode()
        print(sign(quote))

key = sha256(str(x).encode()).digest()
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = open("flag.txt", "rb").read()
enc = cipher.encrypt(pad(flag,16))
print(enc.hex())
print(iv.hex())
```
