<h1 align="center">latex公式测试</h1>
###不变分布
**定理** 在一个不可约的其所有状态都是遍历的链中，极限
\begin{equation}
u\_k = \lim\limits\_{n\rightarrow\infty}p\_{jk}^{(n)}
\label{equ:1}
\end{equation}
恒存在而且不依赖于初始状态$j$，此外$u\_k>0$，
\begin{equation}
\sum u\_k = 1
\label{equ:2}
\end{equation}
且
\begin{equation}
u\_j = \sum\limits\_{i}u\_ip\_{ij}
\label{equ:3}
\end{equation}
反之，假定链是不可约的非周期的，而且存在数列$u\_k\geq 0$满足\eqref{equ:2}和\eqref{equ:3}，则所有状态都是遍历的，$u\_k$均由\eqref{equ:1}所给出且
\begin{equation}
u\_k = \frac{1}{u\_k}
\end{equation}
其中$u\_k$是$E\_k$的平均循环时间.

###标量函数$f(X)$的Jacobian矩阵辨识
考虑标量函数$f(x)$，其变元为$m\times n$实矩阵$X = [x\_1, \cdots , x\_n] \in \mathcal{R}^{m\times n}$。记$x\_j = [x\_{1j}, \cdots , x\_{mj}]^T, j=1, \cdots, n$，则标量函数$f(x)$的全微分为
\begin{equation}
\begin{split}
df(X) &= \frac{\partial f(X)}{\partial x\_1} dx\_1 + \cdots + \frac{\partial f(X)}{\partial x\_n} dx\_n \newline
&= [\frac{\partial f(X)}{\partial x\_{11}},\cdots,\frac{\partial f(X)}{\partial x\_{m1}}]
\left[
\begin{array}
ddx\_{11}\newline
\vdots\newline
dx\_{m1}
\end{array}
\right]
+ \cdots + [\frac{\partial f(X)}{\partial x\_{1n}},\cdots,\frac{\partial f(X)}{\partial x\_{mn}}]
\left[
\begin{array}
ddx\_{1n}\newline
\vdots\newline
dx\_{mn}
\end{array}
\right]\newline
&=[\frac{\partial f(X)}{\partial x\_{11}},\cdots,\frac{\partial f(X)}{\partial x\_{m1}},\cdots,\frac{\partial f(X)}{\partial x\_{1n}},\cdots,\frac{\partial f(X)}{\partial x\_{mn}}]
\left[
\begin{array}
ddx\_{11}\newline
\vdots\newline
dx\_{m1}\newline
\vdots\newline
dx\_{1n}\newline
\vdots\newline
dx\_{mn}
\end{array}
\right]\newline
&=\frac{\partial f(x)}{\partial vec^T(X)}d(vecX) = D\_{vecX}f(X)d(vecX)
\end{split}
\end{equation}