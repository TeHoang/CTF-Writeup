# fizzbuzz102
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     290   |     14    |

## Description
```
did you really think i wasn't going to add an lcg challenge somewhere
```

Phần tiếp theo của fizzbuzz101, thay vì tính $pt \equiv ct^d \pmod{n}$ thì giờ đề bài sẽ tính $pt \equiv a*ct^d + b \pmod{n}$ 

## Solution
Chúng ta hoàn toàn có thể áp dụng kỹ thuật như fizzbuzz101 để tìm $a$, sau đó ta chỉ cần nhân $a^{-e}$ vào $ct$
