# PolyLCG
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     100   |     79    |

## Description
```
I'm so bad at LGC i mean't LCG help me !
```

## Overview

We are given $c_x$ and $c_y$, each of which contains 3 integers and a modulo $p$, ciphertext $ct$

If we have $x_i$ and $y_i$ as the current state for $x$ and $y$, $x_{i+1}$ and $y_{i+i}$ will be calculated by the following formula:

<!-- ```math -->
$$
\begin{aligned}

x_{i+1} &\equiv c_{x, 0} + c_{x, 1}x_i + c_{x, 2}x_i ^2 \pmod{p}\\
y_{i+1} &\equiv c_{y, 0} + c_{y, 1}y_i + c_{y, 2}y_i ^2 \pmod{p} \\
\end{aligned}
$$

The encryption function encrypt the $flag$ bit by bit:

Convert the $flag$'s value to binary with 512 digits

If the $bit_i$ of the $flag=1$, append $x_i$ to the ciphertext, else $y_i$. Calculate $x_{i+1}$ and $y_{i+1}$ then repeat the process for $bit_{i+1}$

## Solution

Since the $flag$ is converted to binary with 512 digits, it's safe to assume that $flag <= 2^{512} = 256^{64}$ which is 64 letters. If the $flag$ has less than $64$ letters, say $63$ then $bit_0 = 0$ which implies that $ct_0 = y_0$. Now we already know $y_0$, we just have to check whether $y_1 = ct_1$, if yes then append $0$ else $1$


