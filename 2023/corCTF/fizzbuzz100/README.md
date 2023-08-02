# fizzbuzz100
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     121   |     134    |

## Description
```
lsb oracles are pretty overdone... anyway here's fizzbuzz
```

Đề cho mình gửi $ct$ đến server và tính $ct^d \pmod{n}$, nếu $pt = flag$ thì sẽ disconnect còn nếu như $pt \equiv 0 \pmod{3}$ thì ta có out = "Fizz", $pt \equiv 0 \pmod{5}$ thì có out = "Buzz", $pt \equiv 0 \pmod{15}$ thì sẽ có "FizzBuzz". Nếu như $(pt, 15) = 1$ thì ta sẽ có được $pt$

## Solution
Gửi cho server $r^{e}ct$ sao cho $(r, 15) = 1$ , lúc này ta sẽ có được $pt = (r^{e} ct)^d \equiv rflag \pmod{n}$. Nhân $r^{-1}$ vào $pt$ thì ta sẽ có được $flag$
