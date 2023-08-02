# fizzbuzz101
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     251   |     19    |

## Description
```
'but in real fizzbuzz you say the number' - someone, probably
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
