# cbc
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     152   |     59    |

## Description
```
who on earth is putting CLASSICAL BORING CRYPTOGRAPHY in my ctf
```

## Solution
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

Ta chuyển thành $c'_i \equiv a_i + k_i \pmod{26}$ để giống như vigenere-cipher sau đó quăng lên [dcode](https://www.dcode.fr/vigenere-cipher) để decode...