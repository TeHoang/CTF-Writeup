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
