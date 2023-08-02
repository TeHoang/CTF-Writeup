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
