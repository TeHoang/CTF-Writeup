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