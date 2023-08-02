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