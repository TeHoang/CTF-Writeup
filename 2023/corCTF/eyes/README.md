# eyes
|**Tag** | **Points** | **Solves**|
|:------:|:----------:|:---------:|
|crypto  |     140   |     75    |

## Description
```
can you see it?
```

## Solution
Note:
```math
$$
\begin{aligned}
A &= 
\left(\begin{array}{cc} 

a_{0,0} & a_{0,1}   &  \dots & a_{0,N-1}          \\
0       & a_{1, 1}  &  \dots & a_{1,N-1}         \\
\vdots  & \ddots    &        & \vdots        \\
0       & \dots     &  0     & a_{N-1, N-1}
\end{array}\right) \\
\\
B &= \left(\begin{array}{cc} 
b_0   \\
b_1      \\
\vdots     \\
b_{N-1}     
\end{array}\right) 
\\ \\
C &= flag
\end{aligned}
$$
```
Sau một hồi quan sát code và nháp thì chúng ta sẽ có các đẳng thức sau:
```math
$$
\begin{aligned}
L_0 &= a_{0,0} + b_0 + flag \\
L_1 &= a_{1, 1} + b_1 + flag \\
L_2 &= a_{0, 0} + a_{0,1} + a_{1,1} + b_0 + b_1 + flag \\
L_3 &= a_{2,2} + b_2 + flag \\
L_4 &= a_{0,0} + a_{0,2} + a_{2,2} + b_0 + b_2 + flag \\
L_5 &= a_{1,1} + a_{1,2} + a_{2,2} + b_1 + b_2 + flag \\
L_6 &= a_{0,0} + a_{0,1} + a_{0,2} + a_{1,1} + a_{1,2} + a_{2,2} + b_0 + b_1 + b_2 + flag

\end{aligned}
$$
```
Ta thu được $flag$ bằng $L_0 + L_1 + L_3 + L_6 - L_2 - L_4 - L_5$
