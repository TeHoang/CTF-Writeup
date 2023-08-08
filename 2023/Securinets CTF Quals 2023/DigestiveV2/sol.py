from fastecdsa.curve import P192
from fastecdsa.point import Point
from Crypto.Util.number import bytes_to_long,inverse, long_to_bytes
from secrets import randbelow
from string import ascii_uppercase
import json
from pwn import * 
from sage.all import * 
from Crypto.Random import get_random_bytes

O=6277101735386680763835789423176059013767194773182842284081
d=randbelow(O)
G=Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811,curve=P192)
P=d*G

def pub_hash(m):
     return (bytes_to_long(m.encode())%O)>>60 
def ecdsa_sign(m):
        h = pub_hash(m)
        k = randbelow(O)
        r = (k * G).x % O
        s = (inverse(k, O) * (h + r * d)) % O
        return json.dumps({"r":r,"s":s})
def verify(msg,r,s):
    h=pub_hash(msg)
    if r > 0 and r < O and s > 0 and s < O:
        u1=(h*inverse(s,O))%O
        u2=(r*inverse(s,O))%O
        V=u1*G+u2*P
        if r==V.x:
            return True
    return False

def solve():
    with remote('crypto.securinets.tn', 8989, level = 'debug') as r:
        r.recvuntil('verification\n')
        r.recvline()
        s = string.ascii_uppercase
        name1 = ""
        for i in range(40):
            name1 += s[randint(0, len(s) - 1)]
        print(f"testing name: {name1}")
        to_send = json.dumps({"option": "sign", "name": name1})
        r.sendline(to_send)
        rec = json.loads(r.recvline())
        s, r_ = int(rec['s']), int(rec['r'])
        pref = '{"username": '
        post_1 = '", "admin": "false"}'
        post_2 = '", "admin": "truee"}'

        m = []
        for i in range(40):
            m.append([pow(256, len(post_1) + 39 - i)] + [0] * i + list([1]) + [0] * (39 - i))
        m.append([O] + [0] * 40)
        m = Matrix(ZZ, m)
        m = m.LLL()
        print(m[0])

        name2 = ''
        for i in range(1, len(m[0])):
            name2 += chr(ord(name1[i - 1]) + int(m[0][i]))
        print(f"name2: {name2}")
        send1 = pref + name1 + post_1
        send2 = pref + name2 + post_2
        
        try:
            assert pub_hash(send1) == pub_hash(send2)
            # Sometime it passes and still fails WTF, maybe I'm just bad at coding 
            to_send = json.dumps({"option": "verify_admin", "name": name2, "r": r_, "s": s})
            r.sendline(to_send)
            r.recvline()
        except AssertionError:
            print(pub_hash(send1))
            print(pub_hash(send2))
solve()

# Securinets{a9e754f12dbce644015061f298ae3fd7cd602846}


