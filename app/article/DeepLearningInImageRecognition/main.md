<h1 align="center">深度学习在图像识别中的应用</h1>
#控制论与机器学习
控制论其本质，在于利用已有的信息抑制系统熵的增加，需要注意的是，这里的熵并不是指热力学中的热力熵或信息论中的信息熵，而应理解为熵的原始定义，即对混乱的度量。既然是度量，便需要一个准则，正如测量一个物体的长度需要一把刻度尺，但不同的刻度尺将得到不同的测量结果，同理，对混乱的不同定义，也将得到不同的控制效果。例如，在温度控制系统中，让温度保持在一个较高的温度或较低的温度均是抑制熵增的行为，因为两者对熵的定义不同。对于孤立系统，熵总是朝着增加的方向移动，但也有例外，此时系统必须是非孤立的，能够收到外界的控制，比如有机体具有熵减趋势，因为DNA是有序的（尽管我们目前仍无法完全理解它），其中起到控制作用的外力是自然选择。控制论所要做的，便是引入外力作用，即反馈，或者说控制环节，以之降低系统的混乱程度，得到我们的期望输出。
##白盒模型与经典控制论
经典控制论中，为了实现对一个系统的控制，我们往往需要先由系统的结构开始分析，利用牛顿力学、电磁原理、热力学等物理原理对系统特性建立微分方程，将其转换为复域的传递函数后，再利用根轨迹或频域分析设计控制环节。如图1所示的简单RLC网络中，假定我们以$u_i(t)$作为输入，$u_o(t)$作为输出，那么此时我们所拥有的信息是整个系统的结构，所需要抑制的混乱就是控制$u_0(t)$朝着我们的期望输出迈进。

<center>![简单的RCL网络](DeepLearningInImageRecognition/image/RLC.png "简单的RCL网络")<br><strong>图1</strong> 简单的RCL网络</center>

由于这个系统的结构是已知的，整个系统对于我们而言相当一个白盒。为此，我们可以很容易地根据基尔霍夫回路电压定律建立方程
\begin{equation}\label{equ:KVL}
u_L(t) + u_R(t) + u_o(t) = u_i(t)
\end{equation}
进一步利用电感特性、电容特性、欧姆定律，式\eqref{equ:KVL}可以进一步推导为
\begin{equation}
LC\frac{d^2u_o(t)}{dt^2} + RC\frac{du_o(t)}{dt}  + u_o(t) = u_i(t)
\end{equation}
此时，输入输出的微分方程已建立，下一步便是经典控制论的内容，我们并不打算继续展开细说。在这个例子中，我们可以看出，白盒模型对整个系统是了如指掌的，是可以对其建模的。此时，“利用已有信息抑制系统的熵增”相当于，对系统建立传递函数（利用已有信息），设计控制环节使我们能得到期望输出（抑制熵增）。

##灰盒模型与系统辨识
牛顿一生的工作对自然科学的贡献是无以衡量的，但牛顿生活的时代忽视了一些重要的东西---统计的概念。在牛顿力学中，有一个前提，系统的状态是可测量的，因此，牛顿力学基于一个已给定的精确初始状态之上对系统分析。然而，物理的测量从来都不是精确的，我们对世界的观察也总是片面而不确定的，世界对我们而言是未知的，我们无法完全确定事物的运作机理。例如图1中的电阻R，R=50$\Omega$ 并不是一个严谨的说法，我们不知道物体细分到最小粒子（如果存在的话）后事物是否变得精确，但就目前人类所拥有的知识而言，阻值为50$\Omega$的电阻是不存在的。我们平常所说的50$\Omega$电阻只是一个统计概念，即电阻在50$\Omega$左右的统计结果。延伸到整个系统，图1 的网络也变得不确定，R、L、C均是不精确的值，此时系统变为一个灰盒模型。所谓灰盒模型，即系统的一部分内容是未知的，另一部分内容是已知的的，例如这里，尽管R、L、C的精确值是未知的，但我们依然可以知道其数值的大致范围。

倘若我们再推广一步，R、L、C的大致范围我们也不知道，如何设计该系统的控制环节便是系统辨识所要研究的内容。系统辨识领域中的一个重要的话题是如何解析出一个含有未知参数的系统结构，如果我们可以获取系统的输入输出样本，利用这些样本，配合上含有未知参数的系统结构方程，采取恰当的拟合方法，如最小二乘以及极大似然等，最后可以获取未知参数的近似解，使得这个灰盒模型的灰色褪去（但不会褪为白盒模型），进一步便可设计系统的控制环节。

##黑盒模型与统计机器学习
白盒模型与灰盒模型的讨论均是基于一个前提：我们知道系统整体模型框架，只是某些参数有可能是未知的。但这个前提在实际生活中往往是不成立的，很多时候，我们非但不知道系统的参数，甚至连系统的模型也知之甚少，此时的系统相当于一个黑盒，我们无法了解其内部结构。例如，判断一封100字的邮件是否为垃圾邮件，假设这个行为可以用一个函数来描述，即这个决策背后存在一个真理（或者说函数），通过它，我们输入100个字符，函数的输出告诉我们这封邮件是否为垃圾邮件 ，那么我们便可以通过这个函数来描述这个系统。可以肯定的值，这个函数在邮件完全可分（即不存在一些可能是或可能不是垃圾邮件的情况）的前提下是存在的，因为字符编码是有限的，只需穷举即可得到这个函数的决策面。但这个方法并不现实，假使所有的汉字只有2000个，那么100字的中文邮件将有$2000^{100}$种可能，要穷举是不可能的。另一种做法是寻求语法结构，先对这100字进行分词，再进行语义分析，这个过程也可以描述为一个函数映射过程：假设函数$f(x)$代表分词，$g(x)$代表语义分析，$y$代表系统输出，那么系统的模型可以表述为$y = g[f(x)]$。这种想法早在二十年前就被抛弃，因为自然语言含有强烈的上下文气息。例如在“冬天能穿多少穿多少，夏天能穿多少穿多少”这个例子中，同一句“能穿多少穿多少”在不同的上下文中含有不同的意义。尽管我个人认为这种上下文背后也必然存在一个因果关系，但这种因果关系是在是太难寻找了，所以这种方法也不是一个可行的方案。

统计机器学习的做法是，假定一个模型（这个模型与系统本质的模型关联并不大），利用大量样本训练假设的模型，最后将训练完毕的模型作为本质模型的逼近。与之前讨论的系统辨识相比，两者在训练阶段是类似的，均是利用样本进行参数整定，不同点在于，系统辨识是训练带有强烈先验的模型（比如由具体物理原理推导出的传递函数）的参数，而统计学习训练的是假设模型（比如高斯模型、隐式马尔可夫模型、神经网络、支持向量机等）的参数。

回到垃圾邮件分类的例子中，统计机器学习的一种解决方案是利用朴素贝叶斯分类，这种方法中，所假设的模型是朴素贝叶斯模型。我们首先建立一个含有$d$个元素的垃圾邮件特征字典，比如{ 购买、大促销、店庆$\cdots$ }，此时，任何一封邮件都可以用一个$d$维列向量表示。例如，某封邮件在字典中的元素只包含“购买”，而其他的元素均不包含，那么这封邮件便可以表示为
\begin{equation}
x = [1, 0, 0, \cdots , 0]^T
\end{equation}


如果我们有大量垃圾邮件样本，我们不难统计出字典中各个元素在垃圾邮件中的出现概率$p(x_i|y=1)$，其中，$y$代表样本的标签，若该样本是垃圾邮件，则$y=1$，反之$y=0$，$x_i$代表字典中的第$i$个元素，例如，我们的字典中，$x_1$ = “购买”。建立样本的描述方式后，我们采用朴素贝叶斯公式，计算样本为垃圾邮件时的概率分布
\begin{equation}
\begin{split}
p(x|y=1)&= p(x_1, x_2, \cdot, x_d|y=1)\newline
&=p(x_1|y=1)p(x_2|y=1)\cdots p(x_d|y=1)
\end{split}\label{naiveBayess}
\end{equation}
显然，式\eqref{naiveBayess}在数学上只有在$x_i$均独立时才成立，而本质上，$x_i$并不是独立的（因为存在上下文），这里本应使用全概率公式，而我们之所以假设$x_i$独立的原因是这样做可以降低模型的复杂度。所以说，在统计学习中，假设模型与本质模型的关联往往不大。

模型训练完毕后（即计算$p(x_i|y=1)$），对于一封新收到的邮件，我们只需使用贝叶斯公式即可计算该邮件是垃圾邮件的概率
\begin{equation}
\begin{split}
p(y=1|x) &= \frac{p(x|y=1)p(y=1)}{p(x)}\newline
&=\frac{\prod_{i=1}^d p(x_i|y=1)}{\prod_{i=1}^d p(x_i|y=1) + \prod_{i=1}^d p(x_i|y=0)}
\end{split}
\end{equation}
统计学习更像是一种假设检验，本例子中的朴素贝叶斯，完全抛弃了语义分析，这并不符合自然语言的原理。但实际中，尽管这个模型并不是本质模型，但逼近效果足以让人接受，能工作得很好，因此被很多邮件厂商所采用。

<center>![机器学习系统框图](DeepLearningInImageRecognition/image/ML.png "机器学习系统框图")<br><strong>图2</strong> 机器学习系统框图</center>

如果一定要对机器学习下一个定义，我认为Tom.Mitchell的描述比较恰当：对于某类任务T和性能度量P，如果一个计算机程序在T上以P衡量的性能随着经验E而自我完善，那么我们称这个计算机程序从经验E中学习。如果将这段话转化成系统框图，则如图2所示。

精确性只存在于数学中，现实世界充满了不确定性，难以寻找事物背后的机理。统计学习绕过这套机理，根据设计者的意愿，假设一个模型，利用这个模型逼近事物的机理，相当于把世界看成一个黑盒，并不打算去探索黑盒的内部结构，而是仿造一个黑盒来模拟其工作原理。

#受限玻尔兹曼机
统计学习并不在乎事物的本质是什么，我们更关心的是数据的分布是怎样的，为了描述数据的分布，我们往往引入各种各样的模型刻画这种分布，比如，贝叶斯决策论中我们引入多维高斯分布，支持向量机中我们引入最大间隔分离面等。对于同一个任务，采用不同的模型得到的结果是不一样的，机器学习与模式识别的一个不同点在于，机器学习更注重统计，模式识别更注重于模型。例如，对于同一个任务，机器学习学者可能会假设出多个模型，再根据模型选择理论选取一个最优的模型，而模式识别学者更倾向于先大致分析这个任务更适合使用哪个模型，选取后仔细优化这个模型。尽管两者有一定的差异性，但很多方面两者是共通的，比如神经网络。神经网络并不依赖于具体的任务，也就是说，语音识别可以用神经网络处理，图像识别也可以用神经网络处理，之所以能这样做的一个原因是，神经网络的内部对于我们而言是透明的，如果我们只看重结果，希望有一个模型可以在给定一个输出的时候输出一个决策结果，不需要关心这个结果是怎么得到的，那么神经网络是一个很好的选择。神经网络的种类众多，一个分支是玻尔兹曼机，这种网络灵感源自统计物理中的玻尔兹曼分布与伊辛模型，随后，在这种网络的基础上又发展出一套受限玻尔兹曼机，通过这些网络，都可以建立数据的概率分布描述。

##伊辛模型
伊辛模型是统计物理中描述物质相变的一种模型，是一个相互磁耦合的自旋阵列。比如在铁这种物质中，当温度降到某个程度，微观原子的自旋会表现出一定的倾向性，从而在宏观上产生磁矩，而当温度升高到一定程度时，其自旋就变得随机。

假设某个伊辛模型中有$N$个自旋的原子，对于每个原子，其状态只能取$+1$或$-1$，我们用向量$s$来表示所有原子的状态，亦即$s$代表这个伊辛模型的状态，那么我们定义该伊辛模型处于状态$s$下的能量函数为
\begin{equation}
E(s; W, H) = -~\Big[\frac{1}{2} \sum\limits_{i, j = 1}^{N} w_{ij}s_is_j + \sum\limits_j Hs_j\Big]
\end{equation}


式中， $w_{ij}$代表原子$i$和原子$j$之间的耦合，如果$i$和$j$是相邻的，那么$w_{ij} = C$，否则$w_{ij} = 0$，如果常数$C>0$，那么这个模型是铁磁性的，否则是反铁磁性的。常数$H$代表作用场，$E(s; w, H)$代表能量函数，对于一般化的能量函数，我们也称之为Lyapunov函数。如果将这个能量函数推广到$H$和$W$不是常数的情况，即

\begin{equation}\label{eq:energyFunction}
E(s; W, H) = -~\Big[\frac{1}{2} \sum\limits_{i, j = 1}^{N} w_{ij}s_is_j + \sum\limits_j h_js_j\Big]
\end{equation}
此时我们将得到一个物理学家称之为“自旋玻璃”的模型，这也是神经网络中的“Hopfield网络”。

##玻尔兹曼机
在统计物理中，对于一个具有一定自由度的物理系统，其系统的状态是具有随机性的而不是固定的（比如房间中的氧气分子分布），假设系统处于某个状态$i$的概率为$p_i$，那么当系统与外界达到热平衡时，其概率分布为
\begin{equation}\label{zhengzefenbu}
p_i = \frac{1}{Z_T} e^{-E_i / T}
\end{equation}
式中，$T$代表系统所处的温度，$E_i$代表系统处在$i$状态下的能量，$Z_T$是在$T$温度下为了使得概率满足柯尔莫果洛夫第二公理的归一化常数。这个分布也称之为正则分布或吉布斯分布。


在机器学习中，我们往往自定义一个能量函数，然后通过正则分布建立模型，通过这种基于能量的模型来对数据进行分析。所以正则分布可以看做是机器学习与统计物理间的桥梁。

如果将式\eqref{eq:energyFunction}中的作用场去掉，并改写成矩阵形式，则得到玻尔兹曼机中的能量函数
\begin{equation}
E(s; W) = -~\frac{1}{2} s^TWs
\end{equation}

事实上，在机器学习中我们并不关心常数$T$，则玻尔兹曼分布为
\begin{equation}
p_i = \frac{1}{Z} e^{-E_i}= \frac{1}{Z} \exp\Big[\frac{1}{2} s^TWs\Big]
\end{equation}


对于一个数据对象，假设我们能观察到$n$维特征，但不仅仅代表这个数据只含$n$维特征，因此我们往往引入隐含特征的概念，假设对于一个对象，我们能观察到$v$个特征，那么我们用$v$个节点来表示这些特征，又假设我们自定义隐含的特征为$h$个，那么我们用$h$个节点来代表这个特征。比如图3代表了含有4个可见节点和2个隐含节点的玻尔兹曼网络。

<center>![未拓扑前的玻尔兹曼机](DeepLearningInImageRecognition/image/BM1.png "未拓扑前的玻尔兹曼机") ![拓扑后的玻尔兹曼机](DeepLearningInImageRecognition/image/BM2.png "拓扑后的玻尔兹曼机")<br><strong>图3</strong> 玻尔兹曼机网络构型</center>

由图3可见，在玻尔兹曼机中，可见节点与可见节点之间、隐含节点与隐含节点之间是可以有连接的，因此这是一个反馈网络。层内节点有连接可以大大地增强网络的表达能力，但是也大大地增加了网络的训练难度，因此玻尔兹曼机并没有非常成功地解决人工智能的任务。

##受限玻尔兹曼机
在受限玻尔兹曼机（Restrict  Boltzmann Machine，RBM）中，我们取消层间连接，从而出发后经过若干次“移动”也无法回到原点，因此RBM也可以认为是一个有向无环图。其网络结构图4所示。

<center>![RBM网络构型](DeepLearningInImageRecognition/image/RBM.png "RBM网络构型")<br><strong>图4</strong> RBM网络构型</center>

为了方便往后的讨论，我们约定网络参数的数学符号如下

\begin{equation}
W_{n_h \times n_v } = \left[               %左括号
\begin{array}{cccc}  
w_{1,1} & w_{1,2} &\cdots & w_{1, n_v}\newline
w_{2,1} & w_{2,2} &\cdots & w_{2, n_v}\newline
\vdots  & \vdots & \ddots  & \vdots\newline
w_{n_h, 1} & w_{n_h, 2} & \cdots & w_{n_h, n_v}
\end{array}
\right]%%%%%%%%%%%%%%%%%%%%
\end{equation}
\begin{equation}
v = \left[   
\begin{array}{cccc}  
v_1\newline  
v_2\newline
\vdots\newline
v_{n_v}
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%%%%
h = \left[   
\begin{array}{cccc}  
h_1\newline  
h_2\newline
\vdots\newline
h_{n_h}
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%
b_v = \left[   
\begin{array}{cccc}  
b_{v_1}\newline  
b_{v_2}\newline
\vdots\newline
b_{v_{n_v}}
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%%%%%%% 
b_h = \left[   
\begin{array}{cccc}  
b_{h_1}\newline  
b_{h_2}\newline
\vdots\newline
b_{h_{n_h}}
\end{array}
\right]
\end{equation}
式中，$W_{n_h \times n_v }$代表网络的权值参数，$w_{ij}$代表第$i$个隐含节点到第$j$个可见节点间的连接权值，因此$W_{n_h \times n_v }$的第$i$行代表了通向$h_i$的所有连接的权值， 第$j$列代表了通往$v_j$的所有连接的权值。 $v$代表可见节点的状态，$h$代表隐含节点的状态，$b_v$代表隐含层到可见层的偏置，$b_h$代表可见层到隐含层的偏置。

在RBM中，我们定义其Lyapunov函数如下：
\begin{equation}\label{eq:RBMenergy}
E(v, h) = - \sum\limits_{i=1}^{n_v}b_{v_i}v_i - \sum\limits_{j=1}^{n_h}b_{h_j}h_j -  \sum\limits_{i=1}^{n_v} \sum\limits_{j=1}^{n_h} h_j w_{j, i}v_i
\end{equation}
若将\eqref{eq:RBMenergy}写成矩阵形式，则为：
\begin{equation}
E(v, h) = -b_v^T v - b_h^T h - h^T W v
\end{equation}
由正则分布的定义\eqref{zhengzefenbu}，我们可以得到$v$，$h$的联合分布为
\begin{equation}\label{lian he fen bu}
p(v, h) = \frac{1}{Z} e^{-E(v, h)}
\end{equation}
其中配分函数$Z$为
\begin{equation}\label{partionFunc}
Z = \sum\limits_{v, h}e^{-E(v, h)}
\end{equation}
由于实际中我们往往只能观察到可见节点，因此对联合分布\eqref{lian he fen bu}边缘化得
\begin{equation}\label{p_x1}
p(v) = \sum\limits_h \frac{1}{Z}e^{-E(v, h)} = \frac{1}{Z}\sum\limits_h e^{-E(v, h)}
\end{equation}
这个$ p(v) $总可以写成如下形式：
\begin{equation}\label{p_x2}
p(v) = \frac{e^{-F(v)}}{Z}
\end{equation}
式中，我们称$ F(v)  $为自由能函数，由式\eqref{p_x1}与\eqref{p_x2}，我们不难推出$ F(v)  $为
\begin{equation}\label{freeEnergyDef}
F(v) = -\ln\sum\limits_h e^{-E(v, h)}
\end{equation}

为了继续我们往下的讨论，我们不加证明地引入关于受限玻尔兹曼机的一个定理：

<strong>定理</strong> 在RBM中，在给定可见元状态时，隐含元的激活条件独立；反之，在给定隐含元状态时，可见元的激活条件独立。

此外，我们还需引入一些记号
\begin{equation}
h_{-k} = (h_1, h_2, \cdots, h_{k-1}, h_{k+1},\cdots, h_{n_h})^T
\end{equation}
\begin{equation}
\alpha(k) = b_{h_k} + \sum\limits_{i=1}^{n_v} w_{k, i}v_i
\end{equation}
\begin{equation}
\beta(v, h_{-k}) = \sum\limits_{i=1}^{n_v} b_{v_i}v_i + \sum_{\substack{j=1\newline j\neq k}}^{n_h} b_{h_j}h_j +  \sum\limits_{i=1}^{n_v}  \sum_{\substack{j=1\newline j\neq k}}^{n_h} h_j w_{j, i}v_i
\end{equation}
即$h_{-k}$代表除$k$外的所有隐含元状态，$\beta(v, h_{-k})$代表除$h_k$外所有节点构成的能量函数。因此，总的能量函数\eqref{eq:RBMenergy}可以写为
\begin{equation}
E(v, h) = -\beta(v, h_{-k}) - h_k \alpha(k)
\end{equation}

下面我们来推导隐含层的激活函数，在给定可见节点状态时，对于节点$h_k$，其激活概率为
\begin{equation}\label{equ:prob}
P(h_k = 1| v)
\end{equation}
由定理\ref{theo:iid}，式\eqref{equ:prob}等价于
\begin{equation}
\begin{split}
P(h_k = 1|h_{-k}, v) &= \frac{P(h_k = 1, h_{-k}, v)}{P(h_{-k}, v)}\newline
&= \frac{P(h_k = 1, h_{-k}, v)}{P(h_k=0,h_{-k} , v) +P(h_k=1, h_{-k} , v)  }\newline
&=\frac{1}{1 + \exp\Big(-E(h_k = 0, h_{-k}, v) +E(h_k = 1, h_{-k}, v)  \Big)}\newline
&= \frac{1}{1 + \exp\Big[  \Big(\beta(v, h_{-k})+ \alpha(k)\cdot 0\Big) + \Big(-\beta(v, h_{-k})- \alpha(k)\cdot 1\Big)  \Big]}\newline
&= \frac{1}{1 + e^{-\alpha(k)}}\newline
&=sigmoid\Big(\alpha(k)\Big)
\end{split}
\end{equation}
因此，给定可见层状态时，隐含元$k$的激活概率为
\begin{equation}\label{p(h_k|v)}
P(h_k =1| v) = sigmoid(b_{h_k} + \sum\limits_{j=1}^{n_v}w_{k, j}v_j)
\end{equation}
同理可推导在给定隐含层状态时，可见元$k$的激活概率为
\begin{equation}\label{p(v_k|h)}
P(v_k = 1|h) = sigmoid(b_{v_k} + \sum\limits_{i=1}^{n_k}w_{i, k}h_i)
\end{equation}
由定理\ref{theo:iid}的独立性可知
\begin{equation}\label{p(h|v)}
P(h|v) = \prod\limits_{j=1}^{n_k}P(h_j|v)
\end{equation}
\begin{equation}\label{p(v|h)}
P(v|h) = \prod\limits_{i=1}^{n_v}P(v_i|h)
\end{equation}

在RBM中，我们的目标是训练参数$W$，$b_v$，$b_h$使得模型能成功地刻画出数据分布。为了方便起见，我们记$\theta = (W, b_v, b_h)$，注意，这并不是矩阵合并，而是将所有的参数用$\theta$来代替。

假定我们有一个训练集$S$
\begin{equation}
S = \lbrace v^{(1)}, v^{(2)}, \cdots v^{(i)}, \cdots, v^{(n_s)}\rbrace 
\end{equation}
其中$n_s$为训练样本数，$v^{(i)}$为第$i$个样本且
\begin{equation}
v^{(i)} = [v_1^{(i)}, v_2^{(i)}, \cdots, v_{n_v}^{(i)} ]^T
\end{equation}

由于样本是独立的，因此似然函数为
\begin{equation}
\mathcal{L}(\theta) = \prod\limits_{i=1}^{n_s}P(v^{(i)})
\end{equation}
对应的对数似然为
\begin{equation}
\ell(\theta) = \ln \prod\limits_{i=1}^{n_s}P(v^{(i)}) = \sum\limits_{i=1}^{n_s} \ln P(v^{(i)}) 
\end{equation}

对于整个训练集，我们要优化参数，使得似然最大化，假设我们使用梯度上升方法，则针对某个样本$\hat{v}$ ，参数的更新规则为
\begin{equation}
\theta = \theta + \eta \frac{\partial\ln\mathcal{L}_{\hat{v}} }{\partial\theta}
\end{equation}
其中
\begin{equation}
\begin{split}
\ln\mathcal{L}_{\hat{v}} & = \ln P(\hat{v})\newline
&=\ln\Big[\frac{1}{Z} \sum\limits_h e^{-	E(\hat{v}, h)}\Big] \newline
&= \ln\sum\limits_h e^{-	E(\hat{v}, h)} - \ln Z\newline
%&= \ln\sum\limits_h e^{-	E(\hat{v}, h)} - \ln\sum\limits_{v, h} e^{-	E(v, h)}
\end{split}
\end{equation}
从而
\begin{equation}
\begin{split}
 \frac{\partial\ln\mathcal{L}_{\hat{v}} }{\partial\theta} 
 &=  \frac{\partial}{\partial\theta}\Big[ \ln\sum\limits_h e^{-	E(\hat{v}, h)} \Big] - 
 %\frac{\partial}{\partial\theta}\Big[ \ln\sum\limits_{v, h} e^{-E(v, h)}  \Big]
 \frac{\partial}{\partial\theta}\ln Z
 \end{split}
\end{equation}
由式\eqref{partionFunc}、式\eqref{p_x1}、式\eqref{p_x2}，得
\begin{equation}
\begin{split}
 \frac{\partial\ln\mathcal{L}_{\hat{v}} }{\partial\theta} 
 &=  - \frac{\partial}{\partial\theta}F(\hat{v}) + \frac{1}{Z} \sum\limits_{v}e^{-F(v)}  \frac{\partial}{\partial\theta}F(v) \newline
 &=  - \frac{\partial}{\partial\theta}F(\hat{v}) + \sum\limits_{v} p(v) \frac{\partial}{\partial\theta}F(v)
 \end{split}\label{temp1}
\end{equation}

通过自由能函数$F(v)$对参数$\theta$求偏导，我们有
\begin{equation}
\begin{split}
\frac{\partial}{\partial\theta}F(v)
&= \frac{\sum_h e^{-E(v, h)} \cdot \frac{\partial E(v, h)}{\partial \theta}}
{\sum_h e^{-E(v, h)}}\newline
&= \sum\limits_h \frac{ e^{-E(v, h)}/Z }{\sum_h e^{-E(v, h)}/Z}\cdot
\frac{\partial E(v, h)}{\partial \theta} \newline
&= \sum\limits_h \frac{p(v, h)}{p(v)}\cdot
\frac{\partial E(v, h)}{\partial \theta}
\end{split}
\end{equation}
从而，式\eqref{temp1}等价于
\begin{equation}
\begin{split}
 \frac{\partial\ln\mathcal{L}_{\hat{v}} }{\partial\theta} 
 &=  - \sum\limits_h \frac{p(\hat{v}, h)}{p(\hat{v})} \cdot \frac{\partial E(\hat{v}, h)}{\partial \theta}+ \sum\limits_{v} p(v) \sum\limits_h \frac{p(v, h)}{p(v)}\cdot \frac{\partial E(v, h)}{\partial \theta}\newline
 &=  - \sum\limits_h p(h|\hat{v})\cdot \frac{\partial E(\hat{v}, h)}{\partial \theta}
 + \sum\limits_{v, h}p(v, h)\frac{\partial E(v, h)}{\partial \theta}\newline
 &= -\mathbb{E}_{p(h|\hat{v})}\bigg[ \frac{\partial E(\hat{v}, h)}{\partial \theta} \bigg]
 + \mathbb{E}_{p(v, h)}\bigg[\frac{\partial E(v, h)}{\partial \theta}\bigg]
 \end{split}\label{expectFunc}
\end{equation}
式中，$\mathbb{E}_{p(h|\hat{v})}$为$p(h|\hat{v})$分布下的期望，$\mathbb{E}_{p(v, h)}$为$p(v, h)$分布下的期望。

通过式\eqref{expectFunc}，我们就可以计算相对于某个样本$\hat{v}$的对数似然梯度。式\eqref{expectFunc}中的第一项是容易计算的，因为我们已经推导出了$p(h|v)$的分布形式，即式\eqref{p(h_k|v)}和式\eqref{p(h|v)}。由于我们简记$\theta = (W, b_v, b_h)$，因此我们需要对$W$，$ b_v $，$ b_h $三个参数分别推导梯度公式。
\begin{equation}
\begin{split}
\sum\limits_h p(h|v)\frac{\partial E(v, h)}{\partial w_{ij}}
=&-\sum\limits_h \prod\limits_{k=1}^{n_h} p(h_k|v) h_i v_j \newline
=&-\sum\limits_{h_i} \sum\limits_{h_{-i}} p(h_i|v)p(h_{-i}|v)h_i v_j \newline
=& -\sum\limits_{h_i}  p(h_i|v)h_i v_j \sum\limits_{h_{-i}}p(h_{-i}|v) \newline
=& -\sum\limits_{h_i}  p(h_i|v)h_i v_j \newline
=& -\sum\limits_{h_i}  p(h_i|v)v_j
\end{split}\label{deltaW}
\end{equation}
\begin{equation}
\begin{split}
\sum\limits_h p(h|v)\frac{\partial E(v, h)}{\partial b_{h_i}}
=&-\sum\limits_h \prod\limits_{k=1}^{n_h} p(h_k|v) h_i\newline
=&-\sum\limits_{h_i} \sum\limits_{h_{-i}} p(h_i|v)p(h_{-i}|v)h_i\newline
=& -\sum\limits_{h_i}  p(h_i|v)h_i\sum\limits_{h_{-i}}p(h_{-i}|v) \newline
=& -\sum\limits_{h_i}  p(h_i|v)h_i\newline
=& -\sum\limits_{h_i}  p(h_i|v)
\end{split}\label{deltaHidBais}
\end{equation}
\begin{equation}
\begin{split}
\sum\limits_h p(h|v)\frac{\partial E(v, h)}{\partial b_{vi}}
=& - \sum\limits_h p(h|v) v_i\newline
=&- v_i
\end{split}\label{deltaVisBais}
\end{equation}

尽管我们可以很容易地通过式\eqref{deltaW}、 式\eqref{deltaHidBais}、式\eqref{deltaVisBais}计算式\eqref{expectFunc}中的第一项，但是第二项却无法计算，因为第二项涉及到归一化因子$Z$，这将是$O(2^{n_v+n_h})$复杂度的项，因此我们需要使用马尔可夫链蒙特卡罗方法（MCMC）进行处理。

#马尔可夫链蒙特卡罗方法
蒙特卡罗方法被评为“20世纪十大算法”之一，自20世纪50年代该方法被提出后的几十年里已被学术界与工业界广泛应用。这套方法最初源自于Stan Ulam对纸牌游戏的思考，他试图计算52张卡牌的组合可能，在尝试穷举失败后，他意识到需要一种随机方法去求取近似解而不是花费大量时间求取一个精确解。随后，他找到冯·诺依曼，两人共同完善了蒙特卡罗方法的一些理论，比如重要性采样和舍弃采样。由于蒙特卡罗方法是一整套解决方案，算法众多，其理论贡献不能仅仅归功于这两人，还应包括提出MH算法的Metroplis和Hasting、将蒙特卡罗方法应用到中子扩散问题的Fermi等。20世纪80年代，蒙特卡罗方法被引入机器视觉与人工智能领域，同时，在此之上加入马尔可夫链形成一套新的理论体系。这套理论常用于贝叶斯推断的归一化、边缘化与期望问题，概率论的配分函数问题，最优化问题以及机器学习中的模型选择问题。

##蒙塔卡罗方法核心思想
蒙特卡罗方法的一个应用是计算一个分布下某个函数的期望，现在假设我们要计算一个积分
\begin{equation}\label{equ:int}
I_f = \int_{-\infty}^{+\infty} (2x^2 + x + 1) \frac{1}{\sqrt{2\pi}} \exp\Big(-\frac{1}{2}x^2\Big)dx
\end{equation}
为了简化，我们记
\begin{equation}\label{equ:f(x)}
f(x) = 2x^2 + x + 1
\end{equation}
\begin{equation}
p(x) = \frac{1}{\sqrt{2\pi}} \exp\Big(-\frac{1}{2}x^2\Big)
\end{equation}
那么，式\eqref{equ:int}可以简写为
\begin{equation}\label{equ:MCintFull}
I_f = \int_{-\infty}^{+\infty} f(x)\cdot p(x) dx
\end{equation}

由于$p(x)$恰好是一个标准高斯分布，倘若我们能从$p(x)$中采样得到$N$个独立同分布（i.i.d）样本$\lbrace x_i\rbrace _{i=1}^N$，则积分$I_f$可以近似为
\begin{equation}\label{equ:MCintProx}
I_f \approx \hat{I}_f = \frac{1}{N}\sum\limits_{i=1}^N f(x_i)
\end{equation}
此时，若$N\rightarrow \infty$，根据大数定律，可知
\begin{equation}
I_f = \lim\limits_{N\rightarrow \infty} \hat{I}_f = \lim\limits_{N\rightarrow \infty} \frac{1}{N}\sum\limits_{i=1}^N f(x_i)
\end{equation}

倘若从数学期望的角度上来解释上面的问题，那么积分\eqref{equ:int}可以理解为：我们现在有一个函数$f(x) = 2x^2 + x+ 1$，其自变量$x$符合标准高斯分布，即$x\sim \mathcal{N}(0, 1)$，那么为了计算$f(x)$在分布$\mathcal{N}(0, 1)$下的数学期望，我们可以在分布$\mathcal{N}(0, 1)$中采样出N个独立的样本$\lbrace x_i\rbrace _{i=1}^N$，将这些样本代入$f(x)$，得到$N$个函数值$\lbrace f(x_i)\rbrace _{i=1}^N$，对这些函数值求和取平均后得到的结果即为期望$I_f$的近似值$\hat{I}_f$。显然，其近似程度与$N$有关，$N$越大，采样的样本越多，近似的程度也便越高。

但积分\eqref{equ:int}未免过于特殊，首先，$p(x)$是一个标准高斯分布，这使得我们可以利用一些很成熟的方法来从$\mathcal{N}(0, 1)$中采样出$N$个样本，但如果$p(x)$不是一个高斯分布，也不是一个均匀分布、伽马分布等一些我们常见的概率分布，它只是一个普通得不能再普通的分布 ，此时又该如何解决？其次，积分\eqref{equ:int}只是一维形式，而实际生活中的概率分布往往是高维的，那么高维情况又该如何推广？接下来的几个小节我们将致力于解决以上几个问题。

##舍弃采样
我们先来解决之前提到的第一个问题，如果说$p(x)$不是一个常见的概率分布应该如何解决？例如
\begin{equation}\label{equ:p(x)}
p(x) = 0.3 \frac{1}{\sqrt{2\pi}}\exp\Big(-\frac{(x-2)^2}{2}\Big) + 0.7 \frac{1}{\sqrt{2\pi}}\exp\Big(-\frac{(x+2)^2}{2}\Big)
\end{equation}
当$f(x)$依然设定为\eqref{equ:f(x)}时，概率密度曲线$p(x)$以及函数$f(x)\cdot p(x)$的图像如图5所示

<center>![实际分布$p(x)$与$f(x)\cdot p(x)$的函数图像](DeepLearningInImageRecognition/image/rejectionPxAndfxPx.png "实际分布$p(x)$与$f(x)\cdot p(x)$的函数图像")<br><strong>图5</strong> 实际分布$p(x)$与$f(x)\cdot p(x)$的函数图像</center>


此时，由于$p(x)$并不是一个常见的概率分布，而我们所拥有的一些简单的采样方案基本都是针对于某一类特定的分布而提出的，基于这个原因，这里要想在$p(x)$中采样出$N$个样本并不是一件简单的工作。为此，我们引入舍弃采样来解决在任意分布上采样的问题。

舍弃采样基于这样一个思想：既然我们无法从一个随意的分布$p(x)$上采样，但是可以在一个特殊的分布$q(x)$上采样，比如从高斯分布中采样，那么我们为何不用$q(x)$来逼近$p(x)$呢？为此，我们引入一个分布$q(x)$，称之为提议分布，这个分布需要满足以下条件
\begin{equation}
p(x) < Mq(x),~~~~M<\infty
\end{equation}
式中，$M$是一个定常数，上述约束条件相当于，提议分布$q(x)$与实际分布$p(x)$的比值$p(x)/q(x)$需要在变量$x$的空间$\mathcal{X}$中存在下界$M$。从图像的角度看，提议分布扩大$M$倍后，应该“覆盖”，或者说“包着”实际分布$p(x)$，例如，对于式\eqref{equ:p(x)}的分布$p(x)$，当$M=2.3$且提议分布$q(x)$为
\begin{equation}\label{equ:q(x)}
q(x) = \frac{1}{3\sqrt{2\pi}}\exp\Big(-\frac{(x+1.3)^2}{2\times 3^2}\Big)
\end{equation}
即$q(x)\sim \mathcal{N}(-1.3, 3)$时，实际分布$p(x)$与提议分布$q(x)$的图像如图6所示

<center>![实际分布$p(x)$与提议分布$q(x)$的函数图像](DeepLearningInImageRecognition/image/rejectionPxAndQx.png "实际分布$p(x)$与提议分布$q(x)$的函数图像")<br><strong>图6</strong> 实际分布$p(x)$与提议分布$q(x)$的函数图像</center>



由于提议分布是一个常规的高斯分布，我们有一系列的成熟方法可以在其之上采样出多个样本。假设我们采样得到一个样本后，我们有两种选择：要么接受这个样本，并将这个样本看做是从$p(x)$上采样得到的，要么舍弃这个样本，认为这个样本与$p(x)$采样的样本差距太大，不能看做是$p(x)$的采样样本。

然而，我们什么时候应该接受$q(x)$的样本作为$p(x)$的样本，什么时候又应该拒绝呢？为了刻画这个事件，我们引入了接受概率的概念。假定我们现在已从$q(x)$中采样得到一个样本$x^{(i)}$，则其接受概率$A$我们定义为
\begin{equation}
A = \frac{p(x^{(i)})}{M\cdot q(x^{(i)})}
\end{equation}

计算得到接受概率后，我们以$A$作为接受样本的概率，但在计算机中，没有一种方法直接地描述“以概率A接受样本”这个行为，为了仿真这个行为，我们可以在区间为$[0, 1]$的均匀分布$U(0,1)$上随机生成一个数$u$，若$u< A$则接受样本，否则拒绝。通过这样的方式，我们便可以模拟“以A为概率接受样本”。我们很容易将一个样本推广到$N$个样本的情况，其具体描述如算法1所示。 


<pre><code class="python">
"""
<strong>算法1</strong> 舍弃采样算法
    N: 采样样本容量
    sampling_q: 从q(x)中采样出一个样本
    p、q: p(x)、q(x)
    result: 采样样本
"""

import random

result = []

while len(result) < N:
   x_i = sampling_q()
   u = random.uniform(0, 1)
   A = p(x_i) / (M * q(x_i))
   result.append(x_i) if u < A else None
   
</code></pre>


对于接受概率其定义，一种较为直观的理解是：接受概率$A(x^{(i)})$刻画了$p(x^{(i)})$与$Mq(x^{(i)})$的相似程度。如图6中的A、B、C三点，假设我们可以分别从两个分布中采样得到多个样本，对于$q(x)$而言，采样样本出现在A点附近的概率最大，其次是B点附近，再次是C点附近。然而，对于$p(x)$而言，采样样本出现在B点附近的概率要比出现在C点附近的概率要小，因此，把从$q(x)$中采样得到的样本直接作为$p(x)$的采样样本是不合适的。但由于
\begin{equation}
\frac{p(x_{B\text{附近}})}{M\cdot q(x_{B\text{附近}})} < \frac{p(x_{C\text{附近}})}{M\cdot q(x_{C\text{附近}})}
\end{equation}
B点较小的接受概率使得我们舍弃了$q(x)$采样样本中B点附近大量的样本，C点较大的接受概率使得我们保留了$q(x)$采样样本中C点附近的大量样本，经过舍弃阶段后，我们便可以从$q(x)$的采样样本中筛选出可以刻画$p(x)$性质的样本，因此，舍弃操作可以看做是对样本的纠正。

在$q(x)$定义为式\eqref{equ:q(x)}，$p(x)$定义为式\eqref{equ:p(x)}且$M=2.3$的情况下，图7左图为$q(x)$及采样样本的概率分布直方图，将这些样本经过舍弃后，其分布直方图如图7右图所示。不难看出，尽管样本是从提议分布$q(x)$中采样得到的，但舍弃采样方法可以很好地逼近原始分布，因此我们可以用筛选后的样本间接地作为$p(x)$的采样样本而不再需要从$p(x)$中直接采样。


<center>![$q(x)$与样本分布直方图](DeepLearningInImageRecognition/image/histQx.png "$q(x)$与样本分布直方图") ![$p(x)$与筛选后的样本分布直方图](DeepLearningInImageRecognition/image/histPx.png "$p(x)$与筛选后的样本分布直方图")<br><strong>图7</strong> 舍弃采样的逼近效果</center>

事实上，式\eqref{equ:p(x)}依然过于特殊，其概率密度不过是两个一维高斯分布的线性组合，如果我们将其扩展到二维情形，例如，当真实分布$p(x)$与提议分布$q(x)$分别定义为
\begin{equation}
\begin{split}
p(x) =
& 0.2\cdot \frac{1}{2\pi} \exp\bigg(-\frac{(x+1)^2 + (y+1)^2}{2}\bigg)~ + \newline
& 0.1\cdot \frac{1}{2\pi} \exp\bigg(-\frac{(x-3)^2 + (y+3)^2}{2}\bigg)~ +\newline
& 0.7\cdot \frac{1}{2\pi} \exp\bigg(-\frac{(x-2)^2 + y^2}{2}\bigg) \newline
\end{split}
\end{equation}
\begin{equation}
q(x) = \frac{1}{2\times 2^2 \cdot \pi} \exp\bigg(-\frac{(x-1.5)^2 + y^2}{2\times 2^2}\bigg)
\end{equation}
在$M = 3$时，真实分布与提议分布的图像如图8所示

<center>![全视图](DeepLearningInImageRecognition/image/2Dgaussian.png "全视图") ![剖视图](DeepLearningInImageRecognition/image/2DgaussianPart.png "剖视图")<br><strong>图8</strong> 二维真实分布（彩色）与提议分布（灰色）</center>

以上例子都过于简单，实际中我们遇到的一般都是高维的情形，概率密度也更为复杂。这将会导致一个结果，提议分布$q(x)$为了“包住”真实分布$p(x)$，$M$需要取一个很大的值使得$q(x)$可以覆盖掉最凸出的维度。想象这样一种极端的情形，在一个高维度的$p(x)$中，有一个维度是类似于脉冲的尖峰，此时$M$需要取很大才足以覆盖它，但对于剩余的维度而言，$M$可能只需要一个较小的值便可以覆盖掉它们，为了使约束$p(x)< M\cdot q(x)$恒成立，M需要取最大的值，过大的$M$使得接受概率$A = p(x)/Mq(x)$过小，大规模地舍弃样本将使采样速度变慢甚至无法再可以接受的时间内完成采样。究其原因，其最根本的弊端在于$q(x)$必须满足约束$p(x)< M\cdot q(x)$。为了解决这个问题，我们将引入重要性采样，这种方法可以使我们不受约束地选取任意的$q(x)$。

##重要性采样
回顾章节"蒙塔卡罗方法核心思想"中的讨论，我们为什么要使用舍弃采样？因为蒙特卡罗方法中积分式\eqref{equ:MCintFull}在$p(x)$不是常规的分布形式时难以采样，导致我们无法利用式\eqref{equ:MCintProx}来计算积分。而舍弃采样通过构建一个容易采样的分布$q(x)$，对其采样样本筛选后作为$p(x)$的样本，式\eqref{equ:MCintProx}从而得以进行下去。


式\eqref{equ:MCintProx}之所以能成立，是因为我们利用了点质量函数来逼近概率密度，即
\begin{equation}\label{equ:pn}
p_N(x) = \frac{1}{N}\sum\limits_{i=1}^N \delta_{x^{(i)}}(x)
\end{equation}
式中，$\delta_{x^{(i)}}(x)$为$x^{(i)}$处的脉冲函数。

下面我们将简单证明式\eqref{equ:pn}的正确性

为了得到概率密度$p(x)$，我们在$x$附近以$x$为中心建立一个小区域$A$，其对应的体积为$V_A$，此时我们从$p(x)$中采样出$N$个样本$x_1, x_2, \cdots, x_N$，那么这些样本落入区域A的概率为
\begin{equation}\label{equ:windows}
P(x\in A)\approx \frac{1}{N}\sum\limits_{i=1}^N 1(x_i)
\end{equation}

式中，$1(x_i)$为示性函数，其定义为
\begin{equation}
1(x) = \left\lbrace
\begin{array}[cc]
& 0, & x \in A \newline
1, & x \notin A
\end{array}
\right.
\end{equation}

实际上，式\eqref{equ:windows}的作用类似于窗函数的作用，即根据离散样本估计点密度，但同时，根据连续性我们也可以得到点$x$的概率密度，即
\begin{equation}
P(x\in A) = \int_A p(x)dx
\end{equation}
当区域A为无穷小区域时，即$V_A\rightarrow 0$，区域$A$内的每一点概率密度相等，此时$p(x)$为常数，因此有
\begin{equation}\label{equ:windows_int}
P(x\in A) = \int_A p(x)dx =  p(x)\int_A dx = p(x)V_A
\end{equation}
联合式\eqref{equ:windows}与式\eqref{equ:windows_int}，有
\begin{equation}
p(x)V_A \approx \frac{1}{N}\sum\limits_{i=1}^N 1(x_i)
\end{equation}
则
\begin{equation}
\begin{split}
p(x) &\approx \frac{1}{V_A}\frac{1}{N}\sum\limits_{i=1}^N 1(x_i) = \frac{1}{N}\sum\limits_{i=1}^N \frac{1(x_i)}{V_A}\newline
&=\frac{1}{N}\sum\limits_{i=1}^N \delta(x_i)
\end{split}
\end{equation}
因此\eqref{equ:pn}成立，证明完毕。

倘若我们不采用这种逼近方式，而采用另外一种，在介绍这种方式之前，我们先引入所谓的重要性权值$w(x)$，即
\begin{equation}
w(x) = \frac{p(x)}{q(x)}
\end{equation}
式中，$q(x)$为任意一个分布。此时，新的逼近方式可以陈述为
\begin{equation}
\hat{p}_N(x) = \sum\limits_{i=1}^N w(x^{(i)})\delta_{x^{(i)}}(x)
\end{equation}
对比式\eqref{equ:pn}，我们可以理解为$p_N(x)$中的$1/N$相当于重要性权值恒为$1/N$。引入重要性权值后，积分式\eqref{equ:MCintFull}可以改写为
\begin{equation}
I_f = \int_{-\infty}^{+\infty} f(x)w(x)q(x) dx
\end{equation}
对应的，式\eqref{equ:MCintProx}改写为
\begin{equation}
\hat{I}_f \approx \sum\limits_{i=1}^N f(x^{(i)}) w(x^{(i)})
\end{equation}


如果从另一个角度思考，以上讨论相当于，我们现在有一个目标函数$f(x)$及概率分布$p(x)$，要计算$f(x)$在分布$p(x)$下的期望，由于$p(x)$不是一个常见的分布形式，导致难以利用式\eqref{equ:MCintProx}计算积分， 那么我们构建一个常见的分布形式$q(x)$，将目标函数改写为
\begin{equation}
\hat{f}(x) = \frac{f(x)p(x)}{q(x)} = f(x)w(x)
\end{equation}
则积分式\eqref{equ:MCintFull}变为
\begin{equation}
\hat{I}_f =  \int_{-\infty}^{+\infty} \hat{f}(x)q(x) dx
\end{equation}
此时我们又可以使用类似于式\eqref{equ:MCintProx}的方式来计算积分了。

对比与之前讨论的舍弃采样而言，重要性采样的优点在于$q(x)$不受约束，也不存在舍弃行为，这使得算法效率相对与舍弃采样有所提高。但重要性采样也有其内在缺点，即$q(x)$选取的好坏程度影响着积分的精度，若$q(x)$选取得不好，则需要大量的样本来提高积分精度。刻画$q(x)$好坏的一种准则是最小化$\hat{I}_N f(x)$的方差，即
\begin{equation}
var_{q(x)}\Big[f(x)w(x)\Big] = \mathbb{E}\Big[f^2(x)w^2(x)\Big] - I^2(f)
\end{equation}
由于$I^2(f)$于$q(x)$无关可以摄取，再利用Jensen不等式，有
\begin{equation}
\mathbb{E}\Big[f^2(x)w^2(x)\Big] \geq \mathbb{E}^2\Big[|f(x)|w(x)\Big] = \Big(\int |f(x)|p(x)dx\Big)^2
\end{equation}
因此提议分布可以选取为
\begin{equation}
q(x) = \frac{|f(x)|p(x)}{\int |f(x)|p(x)dx}
\end{equation}
由于分母只是一个归一化常数可以不管，我们现在要做的是在$|f(x)|p(x)$中采样，这看起来似乎没有什么用，实际上也确实没有什么用，毕竟$|f(x)|p(x)$并不似一个容易采样的函数。但它启示我们一点，如果$p(x)$的样本落在的重要域可以使得$|f(x)|p(x)$取值较大，那么采样效率将会非常高，这也是重要性采样的命名来源。

无论是舍弃采样还是重要性采样都是独立采样，即样本之间是独立的，从而采样效率较低。为了提高采样效率，我们可以使用关联采样，即样本之间存在关联，构建样本之间的关联性所要用到的便是著名的马尔可夫链。



##马尔可夫链

在正式引入马尔可夫链之前，我们打算先从一个随机游走的例子入手。想象一个正方形区域内，在某一点放入N个粒子，这些例子随机地朝着各个方向游走。对于每一个粒子而言，每一次游走的步长是相等的，只是角度随机选择。当粒子移动到正方形的边界是，它将被反弹回正方形区域内。直觉上的想象，经过漫长的时间，粒子将漫布在整个正方形区域内。如图9所示是两个随机游走的例子，其中蓝色的初始状态在中心附近，绿色的初始状态在左下角。

<center>![两个随机游走的例子](DeepLearningInImageRecognition/image/randomWalk.png "两个随机游走的例子")<br><strong>图9</strong> 两个随机游走的例子</center>


这个例子类似于布朗运动，有趣的现象是，起始位置的选取并不会影响最终结果---粒子将呈均匀分布。正如一锅未加盐的汤，无论盐从哪个位置撒下，最终整锅汤的咸淡是均匀的。对于某个特定的粒子而言，追中它的轨迹是无意义的，从宏观上看，粒子下一步处于哪个位置与之前的位置无关，只与它当前的位置有关，因为它是经过怎样的路径到达当前的状态对下一步移动到哪里起不到任何作用。

马尔可夫链意识基于同一个原理，假设我们的变量$x$可取得状态有$s$个，那么集合$S = \lbrace x_1, x_2, x_s\rbrace $被称为状态空间，马尔可夫链刻画的是变量$x$在状态空间$S$中各个状态之间迁移的轨迹。类似于随机游走的例子，马尔可夫链的下一个状态与之前的状态无关，之与当前的状态有关，即
\begin{equation}
p(x^{(i+1)} | x^{(i)} \cdots x^{(1)}) = p(x^{(i+1)} | x^{(i)})
\end{equation}
这个性质也被称为马尔科夫性质。对于给定的系统，我们定义某个状态转移到另一个状态的概率为转移概率，即
\begin{equation}
p(x^{(i+1)} | x^{(i)}) = T(x^{(i)} \rightarrow x^{(i+1)})
\end{equation}

如图10中的系统，状态空间为$\lbrace A, B, C\rbrace $，由图中的参数我们容易算得转移矩阵$\mathcal{T}$

<center>![马尔科夫链](DeepLearningInImageRecognition/image/MCfigure.png "马尔科夫链")<br><strong>图10</strong> 马尔科夫链</center>

\begin{equation}
\mathcal{T} = \left[
\begin{array}{ccc}
T(A\rightarrow A)~~ & T(A\rightarrow B)~~ & T(A\rightarrow C)\newline
T(B\rightarrow A)~~ & T(B\rightarrow B)~~ & T(B\rightarrow C)\newline
T(C\rightarrow A)~~ & T(C\rightarrow B)~~ & T(C\rightarrow C)\newline
\end{array}
\right]
=\left[
\begin{array}{ccc}
0 & 0 & 1\newline
0.6 &0 & 0.4\newline
0 & 0.2 & 0.8
\end{array}
\right]
\end{equation}

倘若我们为A、B、C赋予一些实际意义，我们令A代表下雨，B代表多云，C代表晴天，又假设今天的天气为晴天，现在我们要估计10天后的天气状况。首先，我们可以很容易地将今天的天气描述为一个向量
\begin{equation}
x = [1~~0~~0]
\end{equation}
为了计算10天后的天气，用$x$乘以10次转移矩阵后将得到10天后的天气状况，即
\begin{equation}
[1~~0~~0] \times
\left[
\begin{array}{ccc}
0 & 0 & 1\newline
0.6 &0 & 0.4\newline
0 & 0.2 & 0.8
\end{array}
\right]^{10}
=[0.091~~0.151~~0.758]
\end{equation}
也就是说，10天后下雨的概率为0.091，多云的概率为0.151，晴天的概率为0.758。倘若我们假设今天的天气为多云，利用同样的方法，我们可以计算得10天后的天气状况为
\begin{equation}
[0~~1~~0] \times
\left[
\begin{array}{ccc}
0 & 0 & 1\newline
0.6 &0 & 0.4\newline
0 & 0.2 & 0.8
\end{array}
\right]^{10}
=[0.091~~0.151~~0.758]
\end{equation}
我们发现，不管今天是雨天开始多云，计算得到10天后的天气情况是十分接近的（这里完全一样是因为我们舍去了尾部小数），如果读者有兴趣的话可以验证初始状态为晴天是得到的结果也是一样的。也就是说，不管今天的天气如何，对10天后的天气均无影响。


之所以出现这种现象是因为马尔可夫链在第十个周期时已经进入一个我们称之为平稳的状态。类似于之前的随机游走，当经过足够长的时间后，系统的状态与初始状态再无关联，至于系统的结构（也就是转移矩阵）有关。但并不是所有的转移矩阵都能达到平稳，在这里，我们并不打算深入讨论，只给出结论定理

<strong>定理</strong> 如果一个马尔科夫链是各态遍历的，那么存在一个时间$t_s$，当$t>t_s$时，马尔可夫链到达一个平稳分布$x^\star$，其中$x^\star$满足
\begin{equation}
x^\star = x^\star \mathcal{T}
\end{equation}
所谓各态遍历，即要求马尔可夫链是不可约且非周期的，所谓不可约，即所有状态都是有关联的，从某个状态出发，不存在无法到达的状态，所谓非周期，即马尔可夫链不会陷入某几个状态间循环，满足上述两个条件的马尔可夫链我们称它是各态遍历的。

利用马尔可夫链的这个性质，我们就可以实现关联采样。由于初始状态与稳态无关，我们可以随机设置，经过多次随机游走，进入稳态后得到的状态便可以作为一个样本。以上讨论均基于一个前提，即转移矩阵是已知的。然而，实际中，我们并不知道转移矩阵的数值。例如，我们并不知道由晴天转移到多云的概率是0.2，这个数值是我们捏造的。但是一旦转移矩阵知道了，采样问题便迎刃而解，目前成熟的马尔可夫链蒙特卡罗方法整体框架都是类似的，不同的地方往往在于转移矩阵的构造上。

##Metropolis-Hastings算法
与舍弃采样类似，Metropolis-Hastings算法（以下简称MH算法）也存在一个提议分布，这个提议分布定义为$q(x^\star|x)$，不同的是，舍弃采样中的提议分布受一个强约束，即$p(x) < Mq(x)$，而MH算法中的提议分布只需要满足$q(x^\star|x)>0$即可，显然这个约束相当于没有约束，因为概率论三大公理的第一条就使这个约束成立了。另一个不同点在于，MH算法中的提议分布其意义为：在当前状态$x$下，由提议分布$q(x^\star|x)$产生一个试探性状态$x^\star$，随后根据接受概率决定是否转移到新状态$x^\star$上，这里，接受概率定义为
\begin{equation}\label{equ:MHaccept}
A = \frac{p(x^\star)\cdot q(x|x^\star)}{p(x)\cdot q(x^\star|x)}
\end{equation}
此时，若接受概率$A > 1$，则接受这个新状态，否则，以概率$A$接受新状态。若接受了这个新状态$x^\star$，则状态从$x$转移到$x^\star$处，并在$x^\star$处的提议分布$q(x^{\star\star}|x^\star)$产生一个新的试探状态$x^{\star\star}$，如此反复循环，若不接受这个状态$x^\star$，则状态仍然停留$x$处。

需要注意的一点是，在MH采样中，提议分布$q(x^\star|x)$是对着状态$x$的变动而变动的，例如，如果我们将提议分布$q(x^\star|x)$设计成一个在以$x$为中心，以2为方差的高斯分布，即$q(x\star|x)\sim \mathcal{N}(x, 2)$，那么如图11所示，在$x^{(1)}$状态和$x^{(2)}$状态下的提议分布是不同的。

<center>![不同状态下的提议分布](DeepLearningInImageRecognition/image/diffStateDiffQx.png "不同状态下的提议分布")<br><strong>图11</strong> 不同状态下的提议分布</center>

综合以上的讨论，MH算法可以描述为算法2中的过程。


<pre><code class="python">
"""
<strong>算法2</strong> Metropolis-Hastings算法
    N: 游走次数
    sampling_q(x_i): 从q(x|x_i)中采样出一个样本
    p(x)、q(x, x_i): p(x)、q(x|x_i)
"""

import random

x = random.random()

for step in range(N):
   x_next = sampling_q(x)
   u = random.uniform(0, 1)
   A = (p(x_next) * q(x, x_next)) / (p(x) * q(x_next, x))
   x = x_next if u < A else x
   
return x   
</code></pre>


相比于舍弃采样，舍弃采样的拒绝是直接抛弃样本，而MH采样的拒绝是让样本停留在当前状态。另一个不同点在于，算法2描述的是采样出一个样本的过程，是一个随机游走的过程，而算法1描述的是采样出$N$个样本的过程。尽管算法2只能采样出一个样本，但是我们也可以很容易将其扩展成为采样$N$个样本的算法。另外，由于各个样本的随机游走是独立的，不存在线程安全问题，因此算法2可以很容易设计成为并行算法。

正如我们提到的，如果我们使用一个形式为$q(x^\star|x)\sim \mathcal{N}(x, 2)$的提议分布区采样1000个式\eqref{equ:p(x)}中实际分布$p(x)$的样本，对于不同的游走次数$N$，其结果如图12所示

<center>![N=10](DeepLearningInImageRecognition/image/MH10.png "N=10") ![N=100](DeepLearningInImageRecognition/image/MH100.png "N=100")</center>
<center>![N=1000](DeepLearningInImageRecognition/image/MH1000.png "N=1000") ![N=5000](DeepLearningInImageRecognition/image/MH5000.png "N=5000")</center>
<center><br><strong>图12</strong>不同游走次数下的样本分布直方图</center>

从图中我们不难发现，在游走次数$N=10$是，逼近效果并不完美，随着$N$的增大，当$N=100$时，采样结果已经能很好地刻画实际分布了。此时，$N$再增大（比如1000或5000）已经差别不大了。从随机游走的角度上看，可以理解为，$N=100$时就已经进入平稳分布了，再继续游走下去并没有太大意义。

MH采样可以认为是很多MCMC方法的模板，其他的MCMC方法大多都是MH算法的特例。之所以会从MH算法中衍生出这么多的分支是因为MH有其自身的局限性。首先，我们难以估计状态是否进入平稳状态，即游走次数$N$难以确定。其次，MH算法在高维问题中的效果并不好，因为高维空间的地形复杂，MH算法一不小心就会落入一个周围状态的接受概率都很小的区域，这将导致试探状态不断地被否决，从而长时间留滞在该点附近。接受概率的存在，使得游走效率低下，而Gibbs采样时MH采样的一个特例，这种方法不存在接受概率，或者说接受概率为1，因此每一次游走都将得到一个新的状态，这个特性将大大地加快收敛速度。

##Gibbs采样

Gibbs采样又称为热浴方法或“Glaber动力学”，常用于解决高维分布中的采样问题。假设我们有一个$d$维向量$x$，并且知道任一分量的条件概率分布形式
\begin{equation}
p(x_j|x_{-j}) \triangleq p(x_j|x_1, \cdots, x_{j-1}, x_{j+1}, \cdots x_d)
\end{equation}
则我们构建提议分布

\begin{equation}\label{equ:GibbsQx}
q(x^\star|x) = \left\lbrace 
\begin{array}{cc}
p(x^\star_j|x_{-j}) & \text{若} x^\star_{-j} = x_{-j}\newline 
0 & \text{其他}
\end{array}
\right.
\end{equation}

由于Gibbs采样是MH采样的特例，而MH采样的接受概率公式\eqref{equ:MHaccept}又可以描述为
\begin{equation}\label{equ:MHaccept2}
A = \min\Big\lbrace 1, \frac{p(x^\star)\cdot q(x|x^\star)}{p(x)\cdot q(x^\star|x)} \Big\rbrace 
\end{equation}
将式\eqref{equ:GibbsQx}代入式\eqref{equ:MHaccept2}，并利用$x^\star_{-j} = x_{-j}$性质以及贝叶斯公式，有
\begin{equation}
\begin{split}
A &= \min\bigg\lbrace 1, \frac{p(x^\star)\cdot p(x_j|x^\star_{-j})}{p(x)\cdot p(x^\star_j|x_{-j})} \bigg\rbrace \newline 
&=\min\bigg\lbrace 1, \frac{p(x^\star)\cdot p(x_j|x_{-j})}{p(x)\cdot p(x^\star_j|x^\star_{-j})} \bigg\rbrace \newline 
&=\min\bigg\lbrace 1, \frac{p(x_{-j})}{p(x^\star_{-j})} \bigg\rbrace \newline 
&=1
\end{split}\label{equ:GibbsAccept}
\end{equation}

由式\eqref{equ:GibbsAccept}我们不难得出结论，Gibbs的接受概率恒为1，亦即在Gibbs采样中，我们不存在丢弃样本或状态停滞的行为，每一次都会转移到一个新的状态上，这显然会加快算法的收敛速度。

以上内容未免过于晦涩，为了方便大家理解，我们将再次阐述Gibbs采样的原理。首先，Gibbs采样要基于一个大前提---真实分布$p(x)$在各个维度的条件概率分布是已知的，即$p(x_j|x_1,\cdots, x_{j-1}, x_{j+1}, \cdots, x_d)$已知。如果这个条件概率分布是未知的，则使用Gibbs采样不是一个恰当的策略，应为Gibbs采样的提议分布是基于这个条件概率分布之上构建出来的。式\eqref{equ:GibbsQx}定义的提议分布，其含义为：固定$x_1,\cdots, x_{j-1}, x_{j+1}, \cdots, x_d$这$d-1$个维度的状态不变，单独处理$d$个维度中的一个，即$x_j$。如果将Gibbs采样试想成为一只章鱼，那么每次它都只迈出一只脚，当这只脚固定后，再迈出剩下的另一只脚，因此，Gibbs采样的算法描述如算法3所示。

<pre><code class="python">
"""
<strong>算法3</strong> Gibbs采样算法
    N: 游走次数
    d: 向量x的维度
    p(x[0], ..., x[i]=None, x[d-1]): 
        给定x_0, ..., x_{i-1}, x_{i+1}, ..., x_{d-1}条件下采样出P(x_i | x_1, ..., x_{i-1}, x_{i+1}, ..., x_d)
"""

import numpy as np

x = np.ones(d)

for step in range(N):
    x[0] = p(x_0=None, x_1=x[1], .... x_{d-1} = x[d-1])
    x[1] = p(x_0=x[0], x_1=None, .... x_{d-1} = x[d-1])
                            :
                            :
    x[i] = p(x_0=x[0], x_1=x[1], .... x[i]=None, ..., x_{d-1}=x[d-1])
                            :
                            :
    x[d-1] = p(x_0=x[0], x_1=x[1], .... x{d-2}=x[d-2], x_{d-1}=None)
   
return x   
</code></pre>


至此，MCMC的大体内容已讨论完毕，让我们回到《受限玻尔兹曼机》遗留的问题。《受限玻尔兹曼机》中，式\eqref{expectFunc}，即
\begin{equation}
 \frac{\partial\ln\mathcal{L}_{\hat{v}} }{\partial\theta} =  
 -\mathbb{E}_{p(h|\hat{v})}\bigg[ \frac{\partial E(\hat{v}, h)}{\partial \theta} \bigg]
 + \mathbb{E}_{p(v, h)}\bigg[\frac{\partial E(v, h)}{\partial \theta}\bigg]
\end{equation}
我们说，式中的第一项期望是容易处理的，而第二项却难以处理，因为如果我们采用穷举的方法解决这个问题，这将会是一个$O(2^{n_v+n_h})$复杂度的运算，但采用MCMC的方法就很好处理。由于目前我们需要解决的问题是$\frac{\partial E(v, h)}{\partial \theta}$在分布$p(v, h)$下的期望，根据式\eqref{eq:RBMenergy}中对能量函数$E(v,h)$的定义，偏导数非常容易求取。如果我们能在$p(v, h)$中采样出多个样本，那么这个问题便迎刃而解。但采样$p(v,h)$是一件困难的事，幸运的是，我们知道$p(v,h)$的条件概率$p(v|h)$以及$p(h|v)$，即式\eqref{p(h|v)}和式\eqref{p(v|h)}，因此我们完全可以通过Gibbs采样，经过多次状态转移后采样出一个样本，再以同样的方法采样出多个样本，利用这多个样本，加以式\eqref{equ:MCintProx}，便可以算出期望值，整个问题便解决了。

##对比离差

尽管《受限玻尔兹曼机》章节遗留的问题可以通过Gibbs采样解决，但事实上，正如我们前面提及到的，马尔可夫链进入平稳分布的时间难以确定。我们知道，马尔可夫链的初始状态对平稳分布在性质上是没有影响的，但是不同的初始状态会影响进入平稳分布的时间。就如同往汤里加盐，在不同的位置撒下并不会影响最后的咸淡，但会影响盐在水中的扩散速度，Gibbs采样也同理，不同的初始值对收敛速度有影响。如果初始值随机设置，则模型的训练速度十分缓慢。Hinton提出了一种名为对比离差（Contrastive Divergence，简写为CD）的方法，其中心思想是：既然数据出现了，那么说明这个数据是接近于平稳分布的，因此我们令初始值为该数据样本，进行吉布斯采样，所以，对比离差算法如算法4所示。


<pre><code class="python">
"""
<strong>算法4</strong> CD-k算法
    k: 迭代次数
    p_h(v): 给定v的条件下采样出h
    p_v(h): 给定h的条件下采样出v
    sample: 一个数据样本
"""

v = sample

for iter in range(k):
    h = p_h(v)
    v = p_v(h)
    
return v

</code></pre>


算法4也被称为CD-k算法，随着k的增大，采样得到的样本越接近于模型的平稳分布，但在实验中，$k=1$的时候已经能获得很不错的结果，因此我们往往令$k=1$。而得到最终的采样样本$v^{(k)}$后，对数似然的梯度近似为
\begin{equation}
\frac{\partial\ln P(v)}{\partial w_{i, j}} \approx
 P(h_i = 1 | v^{(0)})v_j^{(0)} - P(h_i = 1 | v^{(k)})v_j^{(k)}
 \label{equ:MAMAMA}
\end{equation}

\begin{equation}
\frac{\partial\ln P(v)}{\partial b_{vi}} \approx
v_j^{(0)} - v_j^{(k)}
\label{equ:MBMBMB}
\end{equation}

\begin{equation}
\frac{\partial\ln P(v)}{\partial b_{i}} \approx
 P(h_i = 1 | v^{(0)}) - P(h_i = 1 | v^{(k)})
 \label{equ:MCMCMC}
\end{equation}

CD-k算法可以认为是利用
\begin{equation}
CD_k = -\sum\limits_{h}P(h|v^{(0)})\frac{\partial E(v^{(0)} , h)}{\partial \theta} + \sum\limits_{h}P(h|v^{(k)})\frac{\partial E(v^{(k)} , h)}{\partial \theta}
\end{equation}
来近似
\begin{equation}
\frac{\partial P(v)}{\partial \theta} = -\sum\limits_{h}P(h|v^{(0)})\frac{\partial E(v^{(0)} , h)}{\partial \theta} + \sum\limits_{v, h}P(v, h)\frac{\partial E(v , h)}{\partial \theta}
\end{equation}
利用CD-k，可以很高效地求得参数的增量$\Delta W$、$\Delta b_v$以及$\Delta b_h$，从而训练受限玻尔兹曼机来刻画数据的分布。

#深度置信网络
深度置信网络是由Hinton于2006年提出的一种深度全连接神经网络，全连接的深度神经网络的训练是及其困难的，然而在深度置信网络中，我们采用网络的逐层训练，随后对网络参数的微调，这种策略使得我们可以容易地训练多层神经网络。由于深度置信网络本质是一种传统神经网络的推广，在本章中，我们将从传统神经网络说起，介绍其训练方法，逐步将其推广到深度置信网络。

##神经网络组成及表达能力
一个神经网络往往由多层神经元组成，神经元作为网络的基本单元，在给定恰当的激活函数和权值的前提下，只要这个网络足够庞大，足以容纳较多的神经元，那么这个网络可以表达任何一个连续函数，当然这只是一个理论上成立的理想情况，实际工程中，我们没有办法利用神经网络来描述所有的函数，但是这个定理能使我们对神经网络的表达能力充满信心。

###神经元 
一个神经元如图13所示，它包含$d$个输入$x = [x_1, x_2\cdots, x_d]^T$以及对应的$d$个权值$w = [w_1, w_2\cdots, w_d]^T$，还有一个偏置$b$。此外，它还应包括一个执行非线性映射的激活函数$f(~\cdot~)$


<center>![神经元](DeepLearningInImageRecognition/image/NNnode.png "神经元")<br><strong>图13</strong> 神经元</center>



与$d$个输入$x = [x_1, x_2\cdots, x_d]^T$直接相连的是数据的输入，例如，一章$28\times 28$像素的灰度图像作为网络输入，由于该图像可以展开成$28\times 28 = 784$的列向量，因此这个例子中的神经元就应该有784个输入，即$x = [x_1, x_2\cdots, x_{784}]^T$。$d$个权值$w = [w_1, w_2\cdots, w_d]^T$，刻画了$d$个输入$x = [x_1, x_2\cdots, x_d]^T$的重要性，$w$中的某个分量$w_i$越大，说明对应的分量$x_i$对最后决策结果的影响越大。从生物学的角度上看，$x$相当于给予生物各种刺激，$w$相当于该生物对各种刺激的敏感度。
例如，我们利用神经元设计一个医学诊断系统来判定一个人是否需要住院观察，对于该神经元，假设输入为$x = [\text{心脏疼痛},\text{头疼},\text{腰疼}]$，如果有某个症状，则对应位置1，否则置0。显然，若一个人心脏疼痛，我们更倾向于让他住院观察，因此我们为心脏疼痛对应的权值设定一个较大的权值$w_1 = 0.9$，头疼次之，我们设定为$w_2 = 0.5$，当一个人腰疼时，不太可能需要住院治疗，我们为其设定一个较小的偏置$w_3 = 0.1$。因此，这个神经元的权值为
\begin{equation}
w = [0.9, 0.5, 0.1]^T
\end{equation}

假设现在有一位患者来到医院，他既有头疼又有心脏疼痛的症状，那么这位患者可以表示为向量
\begin{equation}
x = [1, 0, 1]^T
\end{equation}
此时，病情积累的严重性为
\begin{equation}
w^Tx = 0.1+0.9 = 1
\end{equation}
那么这位患者是否需要住院呢？为此，我们利用前面提及到的偏置$b$来刻画这件事。假设$b = 0.7$，如果$w^Tx>b$，则说明这位患者患有严重的疾病，需要住院观察，网络输出$y=1$，否则这位患者不需要住院，网络输出$y=0$。如果我们定义为神经元的净激活为
\begin{equation}
net = w^Tx + b
\end{equation}
净激活可以理解为排除偏置干扰后神经元接收到的刺激总和。那么上述判别过程相当于用一个阶跃函数对净激活作一个非线性映射，即
\begin{equation}
y = f(net) = \left\lbrace 
\begin{array}{cc}
1 & \text{若}w^Tx - b> 0 \newline
0 & \text{其他}
\end{array}
\right.
\end{equation}

其中，由于$b$是一个常数，因此$w^Tx +b$与$w^Tx - b$并没有区别。但实际上，$b = 0.7$时的神经元做出的决策，其结果只由心脏疼痛这个因素决定，因为如果一个患者没有心脏疼痛，那么最大的净激活是在他即患有头疼又患有腰疼的情况下取得，此时$net=0.6$。而$0.6<0.7$，并不会让他住院。因此，上面的神经元，转换成等价的逻辑命题便是：如果一个人的症状中含有心脏疼痛，则需要住院，否则不需要住院。如果我们把偏置调低，另$b=0.55$，则此时等价的逻辑命题为：如果一个人的症状中含有心脏疼痛，或者症状中既含有头痛有含有腰疼，则需要住院，否则不需要住院。综合以上讨论，偏置起到的是阈值的作用，但是这个阈值取多少就是设计者的意愿了，不同的阈值一般情况下会等价于不同的逻辑命题，这取决于系统的期望输出是什么。

神经元总能转换成一个对应的逻辑表达，需要提出的一个因果关系是，我们并不是从逻辑表达中推出神经元的参数，而是从神经元的参数中可以得到一个逻辑表达。神经元的优点在于，通过一个神经元，便可以实现一个简单的决策，如果拥有更多的神经元，将他们组合起来形成一个神经网络，便可以实现更为复杂的决策行为。这个决策的因果关系是由参数决定的，后面我们将会看到，参数是通过统计学习学到的，因此在神经网络中，我们不需要对事物的因果关系进行分析，只需要使用大量的数据让网络学习其中的因果关系，这些因果关系对于我们而言是透明的。

###逻辑表达
在本小节，我们将再一次讨论网络的逻辑表达能力，如图14 所示的一个接收两维输入的神经元，其偏置$w = [-2, -2]^T$，偏置$b=3$

<center>![与非门的神经元表达](DeepLearningInImageRecognition/image/NNnodeXY.png "与非门的神经元表达")<br><strong>图14</strong> 与非门的神经元表达</center>

如果我们的输入至少有一个为假，即$x = [0,0]^T$或$x = [1,0]^T$或$x = [0,1]^T$，则网络的输出为真，即$y=1$，若两个输入都为真，即$x = [1,1]^T$，则网络的输出为假，即$y=0$。事实上，图\ref{img:NNnodeXY.png}等价于逻辑电路中的与非门，即
\begin{equation}
y = \overline{ x_1\cdot x_2}
\end{equation}
由于与非门是通用们，可以利用多个与非门构建出三大逻辑门：与门、或门、非门。因此，利用图\ref{img:NNnodeXY.png}中的神经元可以表达任意一个逻辑函数。例如，在半加器中，其逻辑函数为
\begin{equation}
y_1 = x_1 \oplus x_2
\end{equation}
\begin{equation}
y_2 = x_1 \cdot x_2
\end{equation}
利用与非门搭建的电路图如图15左图所示，而将其转换成对应的神经网络如图15右图所示(图中，为了美观，我们并没有将偏置画出来)。

<center>![由与非门搭建的半加器](DeepLearningInImageRecognition/image/numberCirc.png "由与非门搭建的半加器") ![由神经元搭建的半加器](DeepLearningInImageRecognition/image/NNCirc.png "由神经元搭建的半加器") <br><strong>图15</strong> 半加器的两种不同描述</center>

我们之所以花费篇幅去介绍神经元的表达能力，是为了说明神经网络确实能实现一些逻辑决策，但并不意味着网络的权值需要我们手工设定的。这里的权值之所以要手工设定，是因为我们精心筛选出来用以阐述神经网络的表达能力，但实际应用中，权值是通过误差传播自动学习的，学习到的权值，其对应的逻辑命题对于人类而言是难以理解的，但这并不重要，因为我们需要的是仅仅决策结果，而不是这个决策是如何产生的因果关系。

##神经网络的前馈
一般而言，神经网络是一个多层结构组织，网络的每一层都由多个神经元阻生，上一层的神经元由下一层的神经元激活。同一层的神经元之间没有连接，因此同一层节点的激活是独立的。神经网络接收到一个数据后，逐层地激活各层的神经元，下一层的输出作为上一层的输入，最后得到一个输出结果。这个过程称为神经网络的前馈或前向传播。

<center>![神经网络的前馈](DeepLearningInImageRecognition/image/3NNfp.png "神经网络的前馈") <br><strong>图16</strong> 神经网络的前馈</center>


如图16所示是一个三层神经网络，由于神经激活是自底向上传播的，如果各层的激活函数都相同，为$f(~\cdot~)$，则网络的第k个节点的输出为
\begin{equation}
z_k = f\bigg[\sum\limits_{j=1}^{n_y} w_{kj} 
f(\sum\limits_{i=1}^{n_x} w_{ji}) + b_j)
+ b_k\bigg]
\label{equ:DBN_NNoutput}
\end{equation}
式中，$w_{kj} $为$y$层的第$j$个节点到$z$层的第$k$个节点之间的连接权值，$w_{ji} $为$x$层的第$i$个节点到$y$层的第$j$个节点之间的连接权值，$b_j$为$y$层第$j$个节点的偏置，$b_k$为$z$层第$k$的节点的偏置。

神经网络的这种自底向上的激活，有时也被解释为特征提取或重新编码。当接收到一个数据时，神经网络将这个数据逐层地进行特征抽取，过滤掉一些冗余信息，将剩余的重新编码，最后利用一个分类器将抽取到的最抽象（即最顶层）特征进行分类，从而完成整个识别过程。

##神经激活

到目前为止，我们只介绍了一种激活函数，即阶跃函数，但实际中我们并不会使用阶跃函数作为激活函数。首先，阶跃函数是不连续的，其次，阶跃函数是不可导的(事实上阶跃函数是可导的，其导函数为脉冲函数，这是一个广义函数，我们不深入讨论)。激活函数不可导，将导致网络无法利用反向传播进行训练，关于这点我们将在反向传播章节讨论。作为激活函数，它应该满足以下几个条件

1. 它必须是非线性的。由式\eqref{equ:DBN_NNoutput}可以看出，若激活函数是线性的，则多层神经网络实际上只相当于两层网络，因为多个矩阵相乘的结果为一个矩阵。网络一旦失去多层结构，则表达能力迅速下降。
2. 它应该具有饱和特性，即至少存在一个上界或下界。饱和特性的存在，使得神经元的输出不至于过高或过低，整个网络的编码维持在一定的范围内。但最近的研究表明，一些近似饱和的激活函数也能工作得很好，如此看来，饱和似乎并不是必要的，但近似饱和还是需要的。
3. 它应该连续且可导。由于反向传播中需要求取激活函数相对于净激活的偏导数，如果激活函数是不可导的，那么反向传播算法将无法执行。

实际工程中，我们常用的激活函数是sigmoid函数(也被称为logistic函数)或双曲正切函数。其中，sigmoid函数我们定义为
\begin{equation}
f(net) = \frac{1}{1+ e^{-net}}
\end{equation}
其对应的图像如图17所示

<center>![sigmoid激活](DeepLearningInImageRecognition/image/sigmoid.png "sigmoid激活") <br><strong>图17</strong> sigmoid激活</center>


可以看到，sigmoid函数是一个值域为$(0,1)$的连续可导函数，其导函数有一个重要特性，即
\begin{equation}
\begin{split}
f'(net) &= \frac{e^{-net}}{(1 + e^{-net})^2} = \frac{1}{1+ e^{-net}} -  \frac{1}{(1+ e^{-net})^2}\newline
&=f(net)\Big[1 - f(net)\Big]
\end{split}
\label{equ:logisticDiff}
\end{equation}

这个特性之所以重要，是应为利用式\eqref{equ:logisticDiff}可以直接通过网络的输出直接计算激活函数相对于净激活的偏导数而不必引入额外的计算。我们看到，sigmoid函数的输出范围为$(0,1)$，有时候，我们希望网络的输出为$(-1,1)$，此时可以使用双曲正切函数，即
\begin{equation}
f(net) = \tanh(net) = \frac{e^{net} - e^{-net}}{e^{net} + e^{-net}}
\end{equation}
其对应的图像如图18所示
<center>![tanh激活](DeepLearningInImageRecognition/image/tanh.png "tanh激活") <br><strong>图18</strong> tanh激活</center>



近年来，在神经网络的研究上又提出了一些新的激活函数，其中最重要的莫过ReLU激活函数，其定义为
\begin{equation}
f(net) = \left\lbrace
\begin{array}{cc}
net & \text{若}net > 0\newline
0 & \text{其他}
\end{array}
\right.
\label{equ:ReLU}
\end{equation}
式\eqref{equ:ReLU}也可以简写为
\begin{equation}
f(net) = \max (0, net)
\end{equation}
其对应的图像如图19所示
<center>![ReLU激活](DeepLearningInImageRecognition/image/ReLU.png "ReLU激活") <br><strong>图18</strong> ReLU激活</center>


这种激活函数相比于sigmoid函数有较大的改进，关于其优点我们将留到反向传播的章节讨论。但ReLU有一个缺点：在$net<0$时导数为0，从而导致反向传播无法更新参数。因此，在ReLU的基础上又产生了一些变体，例如，softplus中，激活函数定义为
\begin{equation}
f(net) = \log(1+e^{net})
\end{equation}
其对应的图像如图19所示

<center>![softplus激活](DeepLearningInImageRecognition/image/softplus.png "softplus激活") <br><strong>图19</strong> softplus激活</center>

从图中不难看出，softplus是ReLU的圆滑版，关于softplus，一个有意思的结论是，其激活函数的导数为logistics函数，即
\begin{equation}
f'(net) = \frac{e^{net}}{1 + e^{net}} = \frac{1}{1 + e^{-net}}
\end{equation}
然而这个结论并没有什么用处，因为它并不能减轻程序的计算量。

ReLU的另一种变体是由He Kaiming等人提出的PReLU，其激活函数定义为\citeup{MS2015}
\begin{equation}
f(net) = \left\lbrace
\begin{array}{cc}
net & \text{若} net >0\newline
\alpha net & \text{若} net \leq 0
\end{array}
\right.
\end{equation}
式中，$\alpha$为一个较小的参数，例如当$\alpha = 0.1$时，其图像如图20所示

<center>![PReLU激活](DeepLearningInImageRecognition/image/PReLU.png "PReLU激活") <br><strong>图20</strong> PReLU激活</center>


显然，PReLU在负半平面不再会出现导数为0的情况。尽管参数$\alpha$需要学习得到，但这种方法在ImageNet 2012数据集上获得了非常好的识别效果，首次在图像识别任务上超越了人的识别效果，错误率仅为4.94\%。在该文中，作者提到了一个有意思的现象：在较低层的网络中，学习到的参数$\alpha$较大，而在高层的网络中，参数$\alpha$较小。作者的猜测是较低曾网络需要尽可能多地保留数据的信息，因此激活函数更倾向于类线性，而高层网络更倾向于抽象数据的结构，从而做出决策，因此高层的激活函数更倾向于非线性。

在同一个任务中，激活函数的不同选取会有不同的实验现象，目前并没有证明哪种激活函数更好。习惯上，在全连接神经网络中，我们更喜欢sigmoid派的激活函数，而在卷积网络中，我们更喜欢ReLU派的激活函数，尽管这些都不是强制的。

##分类器

神经网络的逐层激活，其本质在于将一种编码转化成另一种编码。编码之间的转换，可以过滤掉一些原始编码中无用的噪声或信息，这个过程一般都伴随着熵的减小（但并不绝对）。然而，一个神经网络在最顶层的激活，其编码是人类所无法理解的，因此，在最顶层节点之上还需要一个分类器对神经网络提取到的特征或者说编码进行分类。分类器其作用，一方面在于将编码转换为人类所能理解的编码，这在有监督的分类任务以及无监督的聚类任务中是必要的，因为我们最后希望网络能给我们一个输出标签。但对于降维任务而言有时候并不是必要的，因为降维并不需要输出标签。另一方面，分类器都带有一个准则函数，这个准则函数定义了熵，即定义了什么是混乱，什么是有序。从控制论的角度上看，控制工程中，误差是系统校正的核心，没有误差便没有反馈，没有反馈，则系统难以控制。机器学习也是同样的道理，没有误差，则无法对参数进行校正，机器便无法从样本中学习。误差的来源，源自于准则的定义，即预先预定什么是对的，什么是错的，对于错之间就会存在一个误差，如果机器产生了一个误差，利用这个误差便可以对参数进行校正。神经网络冲，常用的分类器有三种：平方误差、softmax、支撑向量机，尽管支撑向量机是一种重要的分类器，但是鉴于篇幅有限，我们并不打算在本文中介绍支撑向量机，关于其原理读者可参考文献xxxx。

###平方误差分类器
严格来说，平方误差并不能算作一个分类器，它充其量只能算作一个准则，这个准侧除了在神经网络中有应用之外，在很多领域也有广泛的应用。平方误差，或者说二范数，其准则函数定义为
\begin{equation}
L = \sum\limits_{i=1}^d (x_i -t_i)^2
\label{equ:L2error}
\end{equation}
式中，$x_i$为网络的输出，这个输出由输入数据与网络参数共同决定，$t_i$代表标签值，也成为教师信号，由数据的标签值决定，$d$则是$x$的维数。假设一个神经网络的最顶层有4个节点，网络的输出为$[~-0.1~~0.1~~0.8~~0.1~]$，而我们的期望输出是$[~0~~0~~1~~0~]$（再一次强调，这个期望输出由标签值决定），那么实际输出与期望输出之间就会存在一个误差向量$[~-0.1~~0.1~~0.2~~0.1~]$，将其转化成平方误差后为$[~0.01~~0.01~~0.04~~0.01~]$，利用式\eqref{equ:L2error}可以很容易算的此时$L=0.07$。事实上，$L=0.07$对我们而言没有太大用处，它最多只能刻画总的误差量有多大，真正对我们有用的是平方误差向量，利用这个向量，可以将误差反向传播回神经网络的底层，从而自顶向下就网络参数进行校正，关于这个过程更多的细节，我们将会留到反向传播章节介绍。

###softmax分类器
实际中，为了方便分类，我们往往希望网络的输出是“k中取1”的形式，例如，假设我们有四个类别，如果使用二进制编码的话，我们只需两个节点即可，即00代表第一类，01代表第二类，以此类推。如果我们使用所谓的“k中取1”形式，我们便需要四个节点，即0001代表第一类，0010代表第二类，0100代表第三类，1000代表第四类。为了实现“k中取1”的形式，我们需要引入softmax分类器，softmax分类器可以认为是logistics回归的推广，在使用logistics回归进行分类时，只能实现两类分类，而softmax分类器可以实现多类分类功能。

在softmax分类器中，假设容量为$n$的训练集为$S = \big\lbrace (x^{(1)}, y^{(1)}), \cdots, (x^{(n)}, y^{(n)})\big\rbrace $，由于标签$y$的取值可以有$c$种，因此$y^{(i)} \in \lbrace 1, 2,  \cdots, c\rbrace $。我们引入记号$(\phi_1, \phi_2, \cdots, \phi_c)$来表示各个类别的输出概率，由于$\sum\phi_i = 1$，因此记号存在冗余，只需要$c - 1$个记号$(\phi_1, \phi_2, \cdots, \phi_{c-1})$即可，对于$\phi_i$，有
\begin{equation}
\phi_i = P(y = 1; \phi)
\end{equation}
以及
\begin{equation}
\phi_c = P(y = c; \phi) = 1 - \sum\limits_{i=1}^{c-1}\phi_i
\end{equation}
注意，正如我们之前提到的，$\phi$中参数存在冗余，所以$\phi_c$并不是参数，而是一个为了方便后面讨论所引入的一个记号。

由于softmax的概率分布也属于指数分布族，而在指数分布族中，对于概率分布而言，都可以写成如下形式
\begin{equation}\label{equ:expFamily}
P(y; \eta) = b(y) \exp \bigg[\eta^T T(y) - a(\eta)\bigg]
\end{equation}

在softmax中，我们记$T(y) \in R^{c-1}$为

\begin{equation}
T(1) = \left[               %左括号
\begin{array}{cccc}  
1\newline  
0\newline
\vdots\newline
0
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%%%%%
T(2) = \left[   
\begin{array}{cccc}  
0\newline  
1\newline
\vdots\newline
0
\end{array}
\right]~~~~~~%%%%%%%%%%%%%%%%%%%
\cdots~~~~~~
T(c-1) = \left[   
\begin{array}{cccc}  
0\newline  
0\newline
\vdots\newline
1
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%
T(c) = \left[   
\begin{array}{cccc}  
0\newline  
0\newline
\vdots\newline
0
\end{array}
\right]~~~~%%%%%%%%%%%%%%%%%%%%%% 
\end{equation}
记$\Big[T(y)\Big]_i$为$T(y)$的第$i$个元素，记$1 \lbrace \cdot\rbrace $为示性函数，即
\begin{equation}
1 \lbrace A\rbrace  = \left\lbrace 
\begin{array}{cc}
1 & \text{，若命题$A$为真} \newline
0 & \text{，若命题$A$为假}
\end{array}
\right.
\end{equation}
因为$\Big[T(y)\Big]_i = 1\lbrace y = i\rbrace $，因此
\begin{equation}
\begin{split}
\mathbb{E}\bigg[\big[T(y)\big]_i\bigg] &= \big[T(y)\big]_i \cdot P(y = i) \newline
&= P(y=i)  \newline
&= \phi_i
\end{split}
\end{equation}

而
\begin{equation}
\begin{split}
P(y; \phi) &= \phi_1^{1\lbrace y=1\rbrace } \phi_2^{1\lbrace y=2\rbrace }\cdots\phi_c^{1\lbrace y=c\rbrace } \newline
&=\phi_1^{1\lbrace y=1\rbrace } \phi_2^{1\lbrace y=2\rbrace }\cdots\phi_c^{1 - \sum\limits_{i=1}^{c - 1}1\lbrace y = i\rbrace } \newline
&=\phi_1^{\big[T(y)\big]_1}\phi_2^{\big[T(y)\big]_2}\cdots\phi_c^{1 - \sum\limits_{i=1}^{c-1}\big[T(y)\big]_i}\newline
&=\exp\bigg\lbrace \ln\Big[\phi_1^{\big[T(y)\big]_1}\phi_2^{\big[T(y)\big]_2}\cdots\phi_c^{1 - \sum\limits_{i=1}^{c-1}\big[T(y)\big]_i}\Big]\bigg\rbrace  \newline
&=\exp\bigg\lbrace  \Big[T(y)\Big]_1\ln\phi_1 + \Big[T(y)\Big]_2\ln\phi_2+\cdots + \bigg[1-\sum\limits_{i=1}^{c-1}\Big[T(y)\Big]_i \bigg]\ln\phi_c \bigg\rbrace \newline
&=\exp\bigg\lbrace \Big[T(y)\Big]_1\ln\frac{\phi_1}{\phi_c} + \Big[T(y)\Big]_2\ln\frac{\phi_2}{\phi_c} + \cdots  +  \ln \phi_c \bigg\rbrace 
\end{split}
\end{equation}
对比式\eqref{equ:expFamily}，得
\begin{equation}
b(y) = 1
\end{equation}
\begin{equation}
\eta = \Big[~~\ln\frac{\phi_1}{\phi_c}~~~~\ln\frac{\phi_2}{\phi_c}~~~~\cdots~~~~\ln\frac{\phi_{c-1}}{\phi_c}~~\Big]^T
\end{equation}
\begin{equation}
a(\eta) = -\ln\phi_c
\end{equation}
定义
\begin{equation}
\eta_i = \ln\frac{\phi_i}{\phi_c}~~~~~~~~\eta_c = \ln \frac{\phi_c}{\phi_c}=0
\end{equation}
由于
\begin{equation}
e^{\eta_i} = \frac{\phi_i}{\phi_c}
\end{equation}
则
\begin{equation}
\phi_c\cdot e^{\eta_i} = \phi_i
\end{equation}
且
\begin{equation}
\phi_c\sum\limits_{i=1}^c e^{\eta_i}= \sum\limits_{i=1}^c \phi_c e^{\eta_i}
=\sum\limits_{i=1}^k\phi_i
=1
\end{equation}
从而
\begin{equation}
\phi_i = \phi_c e^{\eta_i} = \frac{\exp(\eta_i)}{\sum_{i=1}^c \exp(\eta_i)}
\end{equation}
即
\begin{equation}
P(y=i;\phi) = \phi_i =\frac{\exp(\eta_i)}{\sum_{i=1}^c \exp(\eta_i)}
\end{equation}
以及
\begin{equation}
P(y=i|x;\theta) = \frac{\exp(\theta_i^Tx)}{\sum_{j=1}^c\exp(\theta_j^T x)}
\end{equation}

本质上，softmax分类器都可以看做是一种两层神经网络，与常规的神经网络中使用sigmoid函数作为激活函数不同，在softmax分类器中，激活函数$f(net_k) \propto e^{net_k}$，对应的激活概率定义为
\begin{equation}\label{temp3}
z_k = \frac{e^{net_k}}{\sum_{i=1}^c e^{net_i}}
\end{equation}
式中，$z_k$代表第$k$个节点激活的概率，$net_k$代表第$k$的节点的净激活，取值为输入特征$x$的线性函数，即$net_k = \theta_k  x^T$，$c$为类别的总数。在式\eqref{temp3}中分母的作用下，我们对每个类别的输出都进行了归一化，所以总的激活概率为1。在识别中，计算各个类别的激活概率后，只需选取最大激活概率所对应的类别作为输出类别即可。

#神经网络的反馈
神经网络的反馈是基于准则函数的反馈，准则函数作为误差的度量，刻画了网络的输出与训练集的标签两者之间的差异。整个反馈过程中，实质上就是准则函数最小化的过程，即对网络的参数进行更新，使得误差不断减小。假设一个以参数$\theta$为自变量的准则函数$f(\theta)$，反馈过程就相当于不断寻求$\theta$使得$f(\theta)$最小的过程。如果$f(\theta)$是凸的，即Hessian矩阵是正定的，那么我们称这个问题为凸优化问题，我们可以有很多策略解决凸优化问题，但实际中遇到的问题基本都是非凸问题，解决非凸问题，一个简单有效的方法是利用梯度下降。想象我们在一座山上，为了更快速的下山，我们可以每一步都朝着当前最陡峭的方向（即梯度方向）前进，梯度下降也是基于这个原理，每一次迭代，我们都在当前的$\theta$下计算$f(\theta)$的梯度$\Delta_\theta f(\theta)$，让$\theta$加上这个梯度分量，也就是让它朝着梯度下降的方向迭代。由于梯度下降的每一步都是基于当前的参数$\theta$，所以这是一个贪婪算法，并不能保证收敛到全局最优。如果$f(\theta)$是凸的，那么梯度下降在大部分情况下它会收敛到全局最优（但并不绝对），然而，实际任务由于其非凸性，我们基本上不可能收敛到全局最小值，我们得到的往往是局部极小值。另外，值得一提的是，收敛到全局最小值是没有意义的，因为这个全局最小值是基于训练集的最小值，一旦收敛到此处，意味着网络可以很好地刻画训练集，但并不意味它同样可以很好地泛化到测试集上，这个时候往往会伴随着较高的过拟合风险，我们不应一味地最求全局最小，而应在训练集与测试集两者之间进行一个权衡。梯度下降，因其简单有效的特点，称为优化问题中一个很常用的策略。

##分类器参数校正
20世纪80年代以前，人们并没有找到一个较好的方法训练神经网络，这种状况一直维持到1986年，在这一年里由Rumelhart与Mecelland为首的科学家小组\footnote{事实上反向传播是由很多人在同一年代同时独立提出的} 提出了方向传播算法，首次在神经网络中利用梯度下降逐层地训练网络参数，每训练完一层后将当前层的误差传递回下一层，依次迭代，最后完成整个网络的训练。在这套方法中，核心点有两个：如何利用最顶层（即分类器）的误差来更新最顶层的参数以及如何在某一层网络更新完参数后将该层的误差传播回前一层，我们将会在本小节中讨论最顶层的参数校正，并在下一小节讨论误差传播。
###平方误差分类器参数校正
由于在平方误差分类器中，准则函数定义为
\begin{equation}
J(\theta) = \frac{1}{2}\sum\limits_{i=1}^c(t_i - z_i)^2 = \frac{1}{2}||t-z||^2
\end{equation}
式中，$z_i$为训练集的标签值，而网络的输出$t_i$又是由前一层的静激活经过非线性映射后得到的，即
\begin{equation}
t_i = f(net_i)
\end{equation}
式中，$net_i$为输出层的前一层，即倒数第二层的净激活，而这个净激活又被定义为
\begin{equation}
net_i = wx + b
\end{equation}
式中，$w$为输出层与倒数第二层两者之间的权值，$b$为偏置，因此，我们不难通过链式求导得到误差相对于参数的梯度，即$J(\theta)$相对于$\theta$（这里的$\theta$即为$w$和$b$）的导数
\begin{equation}
\frac{\partial J(\theta)}{\partial w} = \frac{\partial J(\theta)}{\partial net} \frac{\partial net}{\partial w}\label{equ:5.0}
\end{equation}
以及
\begin{equation}
\frac{\partial J(\theta)}{\partial b} = \frac{\partial J(\theta)}{\partial net} \frac{\partial net}{\partial b}\label{equ:5.00}
\end{equation}
如果此时的激活函数是sigmoid函数，那么容易知道
\begin{equation}
\frac{\partial J(\theta)}{\partial net} = net(1-net)\label{equ:5.1}
\end{equation}
如果激活函数是ReLU函数，也容易得到
\begin{equation}
\frac{\partial J(\theta)}{\partial net} = \left\lbrace
\begin{array}{cc}
1 & \text{若}net>0\newline
0 &\text{若}net\leq 0\newline
\end{array}
\right.\label{equ:5.2}
\end{equation}
而$\partial net/\partial \theta$只是一个线性函数，同样容易求得
\begin{equation}
\frac{\partial net}{\partial w} = x~~~~~~~~\frac{\partial net}{\partial b} = 1\label{equ:5.3}
\end{equation}
利用\eqref{equ:5.1}或\eqref{equ:5.2}\footnote{这取决于你的激活函数选取}以及\eqref{equ:5.3}便可以求取式\eqref{equ:5.0}以及\eqref{equ:5.00}中参数应该修改的幅度，即梯度。

###softmax分类器参数校正
在softmax的训练中，由于我们的期望输出为
\begin{equation}
h_\theta(x) =\mathbb{E}\Big[T(y)|x;\theta \Big]
%%%%%%%%%%%%%%%%%%%%%%%%%%%
=\mathbb{E}\left[
\begin{array}{cccc}
1\lbrace y=1\rbrace \newline
1\lbrace y=2\rbrace \newline
\vdots\newline
1\lbrace y=c-1\rbrace 
\end{array}
\right | x; \theta
\left.
\begin{array}{cccc}\newline\newline\newline\newline\end{array}
\right]
%%%%%%%%%%%%%%%%%%%%%%%%%%%
=\left[
\begin{array}{cccc}
\phi_1\newline
\phi_2\newline
\vdots\newline
\phi_{c-1}
\end{array}
\right] 
%%%%%%%%%%%%%%%%%%%%%%%%%%%
=\left[
\begin{array}{cccc}
\frac{\exp(\theta_1^T x)}{\sum_{j=1}^c \exp(\theta_j^T x)}\newline
\frac{\exp(\theta_2^T x)}{\sum_{j=1}^c \exp(\theta_j^T x)}\newline
\vdots\newline
\frac{\exp(\theta_{c-1}^T x)}{\sum_{j=1}^c \exp(\theta_j^T x)}
\end{array}
\right]
\end{equation}
对应的似然函数为
\begin{equation}
\mathcal{L}(\theta) = \prod\limits_{i=1}^n P(y^{(i)}|x^{(i)}; \theta)
\end{equation}
对应的对数似然函数为
\begin{equation}\label{equ:softmaxErr}
\begin{split}
\ell(\theta) &= \sum\limits_{i=1}^n\ln P(y^{(i)}|x^{(i)}; \theta)\newline
&=\sum\limits_{i=1}^n\sum\limits_{j=1}^c \ln \bigg(\frac{\exp(\theta_j^Tx^{(i)})}{\sum_{t=1}^c\exp(\theta_t^T x^{(i)})} \bigg)^{1\lbrace y^{(i)} = j\rbrace }\newline
&=\sum\limits_{i=1}^n\sum\limits_{j=1}^c 1\lbrace y^{(i)} = j\rbrace  \ln \bigg(\frac{\exp(\theta_j^Tx^{(i)})}{\sum_{t=1}^c\exp(\theta_t^T x^{(i)})} \bigg)
\end{split}
\end{equation}
式\eqref{equ:softmaxErr}的相反数也被称为交叉熵，在训练过程中充当准则函数，我们对其求导，有
\begin{equation}
\begin{split}
\frac{\partial \ell (\theta)}{\partial\theta_j} 
&=\sum\limits_{i=1}^n\sum\limits_{j=1}^c 1\lbrace y^{(i)} = j\rbrace \bigg[x^{(i)} - \frac{\partial}{\partial\theta_j}\ln \sum\limits_{t=1}^c \exp\big(\theta_t^T x^{(i)}\big)\bigg]\newline
&=\sum\limits_{i=1}^n\sum\limits_{j=1}^c 1\lbrace y^{(i)} = j\rbrace  \bigg[ x^{(i)} - \frac{\exp(\theta_j^T x^{(i)})}{\sum_{t=1}^c\exp(\theta_t^T x^{(i)})} x^{(i)}\bigg]\newline
&=\sum\limits_{i=1}^n\sum\limits_{j=1}^c 1\lbrace y^{(i)} = j\rbrace  x^{(i)} \bigg[1 - P(y^{(i)} = j|x^{(i)}; \theta)\bigg]
\end{split}
\end{equation}
由于$1\lbrace y^{(i)} = j\rbrace  \in \lbrace 0, 1\rbrace $，所以写成向量形式为
\begin{equation}\label{equ:softmaxGrid}
\frac{\partial \ell (\theta)}{\partial\theta_j}  = \sum\limits_{i=1}^n x^{(i)} \Big[1\lbrace y^{(i)} = i\rbrace  - P(y^{(i)}=j|x^{(i)}; \theta)\Big]
\end{equation}
通过使用式\eqref{equ:softmaxGrid}进行迭代，我们便可以使用梯度上升（下降）进行搜索，从而最大化似然（或最小化交叉熵）来训练softmax分类器。

#误差传播
为了简单起见，我们使用一个三层神经网络对误差传播进行讨论，但通过这里的讨论，我们可以很容易将神经网络扩展到多层结构。

<center>![三层神经网络的网路构型](DeepLearningInImageRecognition/image/3NN.png "三层神经网络的网路构型") <br><strong>图21</strong> 三层神经网络的网路构型</center>

如图中的三层神经网络，$y$层到$z$层为分类器，根据之前的讨论，我们可以利用式\eqref{equ:5.0}和式\eqref{equ:5.00} 求取$\partial J(\theta)/\partial \theta_{yz}$的值，如果我们要求取$\partial J(\theta)/\partial \theta_{xy}$的值，那么通过链式求导，我们有
\begin{equation}
\frac{\partial J(\theta)}{\partial\theta_{xy}} = \frac{\partial J(\theta)}{\partial y} \frac{\partial y}{\partial net_y} \frac{\partial net_y}{\partial \theta_{xy}}\label{equ:xxxxx}
\end{equation}
而我们又可以求得
\begin{equation}
\frac{\partial J(\theta)}{\partial y} =  \frac{\partial J(\theta)}{\partial net_z} \frac{\partial net_z}{\partial y}\label{equ:5.0.5}
\end{equation}
如果我们定义式\eqref{equ:5.0}以及式\eqref{equ:5.00}中的误差为
\begin{equation}
\delta_z = \frac{\partial J(\theta)}{\partial net_z}
\end{equation}
那么我们可以将式\eqref{equ:5.0.5}写为
\begin{equation}
\frac{\partial J(\theta)}{\partial y}  =  \delta_z \frac{\partial net_z}{\partial y} = \delta_z \theta_{yz}^T
\end{equation}
式中，$\partial J(\theta) /\partial y$就是分类器输出层（Z层）的误差传播回其上一层（Y层）的误差，如果我们定义Y层的误差为
\begin{equation}
\delta_y = \frac{\partial J(\theta)}{\partial y} \frac{\partial y}{\partial net_y}
\end{equation}
则我们可以利用后一层传播回来的误差$\delta_z$计算该层的误差
\begin{equation}
\delta_y = \delta_z \theta_{yz}^T  \cdot \frac{\partial y}{\partial net_y}
\end{equation}
从而我们可以利用该层的误差$\delta_y$计算该层参数$w_{xy}$的增量，即梯度
\begin{equation}
\frac{\partial J(\theta)}{\partial\theta_{xy}} =\delta_y \cdot  \frac{\partial net_y}{\partial \theta_{xy}}\label{equ:yyyyy}
\end{equation}
通过式\eqref{equ:yyyyy}对参数$\theta_{xy}$进行校正，校正完毕后，如果网络不止三层，而是四层，假设X层的下一层为P层，那么为了计算连接X层与P层参数$\theta_{px}$的梯度，利用链式求导，同样有
\begin{equation}
\frac{\partial J(\theta)}{\partial\theta_{px}} = \frac{\partial J(\theta)}{\partial x} \frac{\partial x}{\partial net_x} \frac{\partial net_x}{\partial \theta_{px}}\label{equ:zzz}
\end{equation}
与之前的做法类似，我们有
\begin{equation}
\begin{split}
\frac{\partial J(\theta)}{\partial x} & = \frac{\partial J(\theta)}{\partial y}  \frac{\partial y}{\partial net_y}\frac{\partial net_y}{\partial x}\newline
&=\delta_y \cdot \theta_{xy}^T
\end{split}
\end{equation}
同样的道理，X层的误差$\delta_x$定义为
\begin{equation}
\delta_x =   \frac{\partial J(\theta)}{\partial x} \frac{\partial x}{\partial net_x} = \delta_y  \theta_{xy}^T \cdot \frac{\partial x}{\partial net_x}
\end{equation}
则参数$\theta_{px}$的梯度便可以利用$\delta_x$计算
\begin{equation}
\frac{\partial J(\theta)}{\partial\theta_{px}} = \delta_x \cdot \frac{\partial net_x}{\partial \theta_{px}}
\end{equation}
如果还有更多的层，其原理雷同，我们不再详细叙说。现在让我们抛开以上的数学内容从网络的结构上解释这个算法为什么叫做误差反向传播，首先我们观察各层的误差，即
\begin{equation}
[\delta_z~~\delta_y~~\delta_x ] = \bigg[~~
\frac{\partial J(\theta)}{\partial net_z}~~~~~~
\delta_z \theta_{yz}^T  \cdot \frac{\partial y}{\partial net_y}~~~~~~
\delta_y  \theta_{xy}^T \cdot \frac{\partial x}{\partial net_x}
~~\bigg]\label{equ:delta inject}
\end{equation}
式中，$\theta^T$起到的作用是将误差$\delta$反向注入的行为，这个行为如图22所示
<center>![误差反向注入](DeepLearningInImageRecognition/image/3NNbp.png "误差反向注入") <br><strong>图22</strong> 误差反向注入</center>


观察式\eqref{equ:delta inject}，我们不难看出，除了最顶层外，剩余层的误差形式都是类似的，如果用一句话概括反向传播算法，便是：将$\ell$层的误差注入到$\ell - 1$层中，再乘上$\ell -1$层激活函数的导数，得到$\ell - 1$层的误差，利用这个得到的误差，对$\ell - 1$层的参数进行更新，更新完毕后，将$\ell - 1$层的误差重新注入到$\ell - 2$层，重复上述步骤直至误差传遍整个网络。但是这里有个例外，最顶层的误差定义与剩余层的不一样，之所以会这样是因为最顶层的误差并不是通过注入方式得到的，而是人为定义得到的，因为这个误差源自于准则函数。

我们可以看到，反向传播这种策略实际上与前向传播是类似的，反向传播也是一种贪婪算法，这将会导致一些问题。因为每一次误差传播都是更新参数后再将误差注入回前一层，这并不能保证计算得到的梯度就是真实的梯度，一旦网络的层数过深，将会导致前面层的真实导数与利用反向传播计算得到的导数相差过大。另外，如果使用sigmoid函数作为激活函数，它将很容易进入饱和状态，前面层的梯度接近于0，从而参数无法更新，这种现象我们称之为梯度消失。一种对抗梯度消失的方法是将sigmoid函数换成ReLU激活函数，关于ReLU为什么可以抵抗梯度消失的原理目前尚未研究出来，但是实验现象表明它确实能抑制梯度消失。

#深度置信网络
深度置信网路（Deep Belief Networks，简写为DBN）本质就是一种传统的神经网络，但是它在传统神经网络的基础上加入一些变动。首先，这是一种深层的神经网络，而传统的神经网络一般只设计为三层结构。另外，深度置信网络是一个以受限玻尔兹曼机为基础，多个受限玻尔兹曼机垒出来的多层神经网络。图23展示了一个深度为4的深度置信网络。

<center>![DBN网络构型](DeepLearningInImageRecognition/image/DBN.png "DBN网络构型") <br><strong>图23</strong> DBN网络构型</center>


我们之所以采用深度结构，是因为在神经元总数不变的前提下，深度结构的表达能力比浅结构的表达能力更强。之所以要在这个结构中引入受限玻尔兹曼机，是因为传统的深度结构无法训练。正如我们前面提及到的，深度结构会在网络的较浅层出现梯度消失现象，导致浅层无法对参数进行校正。由于数据必须从浅层神经元逐层地传播到深层神经元，一旦浅层的参数无法校正，将会导致深层的网络也无法进行参数校正，因为浅层参数无法校正意味着浅层无法对数据进行合理地重编码，数据经过浅层后得到的是混乱的数据，尽管深层不会产生太大的梯度消失现象，但数据经过浅层的打乱后，数据已经混乱了，训练也便没有意义。另一方面，传统的神经网络初始值设定为随机值，这些随机值一般设定为一个均值为0，方差较小的高斯分布，神经网络是一个非凸问题，局部最小值众多，网络最后收敛到的最小值取很大程度上决于初始值的选取，随机选取初始值虽然是一个可行的方法，但是如果我们能让参数的初始值设定在一个较合理的初始值，将会很大程度地改善网络的收敛性能，而受限玻尔兹曼机一个重要的贡献在于，将深度神经网络的参数初始化到一个较好的值。

深度置信网络的训练分为两个阶段，分别是预训练阶段和参数微调阶段。在DBN的预训练阶段中，将相邻两层看做一个受限玻尔兹曼机，采用受限玻尔兹曼机的训练方法，将原始数据作为最底层的输入，每层RBM隐含层的输出作为后一层的输入，然后进行逐层贪婪的无监督训练。对于每层RBM，其训练过程描述如算法5所示

<pre><code class="python">
"""
<strong>算法5</strong> 受限玻尔兹曼机训练算法
    max_epoch: 训练周期
    S: 训练集
    k: CD-k迭代次数
    p_h(v): 给定v的条件下采样出h
    p_v(h): 给定h的条件下采样出v
    sample: 一个数据样本
    e: 衰减系数
    p: 动量项系数
"""

for epoch in range(max_epoch):
    for sample in S:
        v_t = v_0 = sample
        h_0 = p_h(v_0)
        
        # CD-k
        for i in range(k):
            h_t = p_h(v_t)
            v_t = p_v(h_t)
            
        # 计算增量    
        delta_weight = np.dot(v_t.T, h_t) - np.dot(v_0.T, h_0)
        delta_bias_vis = v_t - v_0
        delta_bias_hid = h_t - h_0
        
        # 更新权值
        weight = e * (p * weight + eta * delta_weight)
        bias_vis += eta * delta_bias_vis
        bias_hid += eta * delta_bias_hid
        
    h = p_h(v)
    v = p_v(h)
    
</code></pre>

算法中，学习率$\eta$、动量项系数$p$以及权衰减系数$e$我们将会留到网络设计技巧中讨论，这些技巧在数学推导的过程中是不必要的，然而在实际工程中是必要的，有时候缺了它们网络训练会失败。当逐层训练完毕后，网络的参数已经初始化到一个较好的位置。在参数微调阶段，接着执行全局的反向传播算法进行有监督的权值微调。通过这样的方法，可以避免单纯地使用反向传播方法中会出现的陷入局部最优问题，由于识别的过程中，数据是逐层地进行维度变化，所以DBN也可以认为是一种特征提取方法，对应的，深度学习有时候也称之为“特征学习”。

#卷积神经网络
卷积神经网络灵感源自哺乳动物的视觉系统，它是唯一一个不需要预训练便能直接训练的深度网络。LeCun在1989年设计了第一个卷积神经网络，并将这个网络运用到邮编数字识别中取得了很好的效果，随后，xxxx将卷积神经网络应用到文档识别中，实现了可理解数字串的网络，这是一个重大的突破。但卷积神经网络在提出的二十多年里一直默默无闻，直到最近几年，人们发现在图像识别中卷积神经网络相比于其他的模型能更好地进行特征提取才被重视。目前，几乎所有最好的识别系统都是基于卷积神经网络的，从某种意义上而言，卷积神经网络相当于深度学习的代言人。

卷积神经网络可以看做是一种特殊的神经网络，在深度置信网络中，网络节点是全连接的，而卷积神经网络中连接是局部的。此外，卷积网络强制权值共享，对比于深度置信网络，卷积网络的这些特性都体现着非常强的正则。

如图24左图所示为传统的全连接神经网络，我们可以看到，每一个上层节点与下层节点都含有连接，而所有的连接都是独立无关联的，即每个连接权值都不相等。对应的，图24右图所示为卷积神经网络，在这种网络构型中，每个上层节点只与部分的下层节点连接，并且，这些连接的权值是共享的，即相同颜色的连接代表其权值相等。局部连接将会大大减少网络的连接数量，而权值共享又会大大减少网络的参数数量。例如在左图中，连接数量为$3\times 5 = 15$，由于权值不共享，其参数数量也是15。而右图的连接数量为$3\times 3$，权值共享使得网络的参数只有3个。卷积网络的设计目的是让网络拥有更多的连接，而拥有更少的权值。尽管这里连接数量上卷积网络要比全连接网络少，但是我们后面将会看到，卷积网络将通过多张特征图构造出更多的连接。

<center>![全连接神经网络](DeepLearningInImageRecognition/image/fullNN2d.png "全连接神经网络") ![卷积神经网络](DeepLearningInImageRecognition/image/convNN2d.png "卷积神经网络") <br><strong>图23</strong> 二维视觉下的全连接神经网络与卷积神经网络</center>

卷积神经网络，一般用于图像识别与声音识别两个领域，因为这两个领域带着明显的二维特性。例如在图像识别中，图像即可以看做是高维的，也可以看做是二维的，如果将它看做高维的，那么就是将像素点展开成为一个高维列向量，展开后的图像将不再具有原始的面貌。如果将它看做是二维的，就是保留图像的原貌，利用二维的平面直角坐标系来描述。声音之所以可以看做二维的，是因为它带有时间这一维度，关于声音识别，我们不过多讨论，更多的细节请参考文献xxxx。

由于卷积网络保留了图像的二维面貌，因此相比于全连接神经网络而言，其网络构型是一个三维构型，如图24左图所示为三维视觉下全连接神经网络。由于上层节点是一个高维列向量，我们可以认为这个向量是一维的，并且这个向量里的每一个元素都与输入图像上的每一个像素点连接，不同元素之间的连接权值是不同的。而图24右图所示是三维视觉下的卷积神经网络，我们可以看到，上层节点是一个二维矩阵，因此它的特征我们可以认为是二维的，这些上层节点组成的二维矩阵我们称为特征图（feature map），特征图里的每一个元素，都只与输入图像上的一小块区域有连接，并且，特征图里的不同元素的连接权值是相等，这些相同的连接权值我们称之为卷积核（convlution kernel）。图中仅仅是一张特征图，实际中的卷积神经网络，往往通过多个不同的卷积核，卷积出多张特征图。

<center>![全连接神经网络](DeepLearningInImageRecognition/image/fullNN3D.png "全连接神经网络") ![卷积神经网络](DeepLearningInImageRecognition/image/convNN3D.png "卷积神经网络") <br><strong>图24</strong> 三维视觉下的全连接神经网络与卷积神经网络</center>

#卷积神经网络的前馈
一个完整的卷积神经网络应包含三个内容：卷积层、采样层以及全连接层，关于各层的细节以及作用我们将在后面的小节中叙述，现在让我们先大致了解卷积神经网络的结构。如图25所示是卷积神经网络其网络构型

<center>![卷积神经网络网络构型](DeepLearningInImageRecognition/image/CNN.png "卷积神经网络网络构型") <br><strong>图25</strong> 卷积神经网络网络构型</center>

在这种结构中，卷积层与采样层交错出现，在网络顶端采用全连接神经网络或其他分类器。图中卷积层里的每一张特征图，其执行过程都如图24右图所示，这些不同的特征图对应着不同的卷积核，多张特征图，增加了网络的连接数目，但由于每张特征图只对应一个卷积核，所以网络的参数（即卷积核）的数目相比与全连接神经网络参数的数目而言是很小的。

#卷积
卷积神经网络所使用的卷积即二维离散卷积，其定义为
\begin{equation}
\begin{split}
y[s, t] &= \sum\limits_{i=1}^{m_1 +  m_2 -1}\sum \limits_{j=1}^{n_1 + n_2 -1} x[i, j]\cdot k[s-i+1, t-j+1]\newline
&~~~~~~~ 1\leq s \leq m_1 + m_2 -1\newline
&~~~~~~~ 1\leq t  \leq n_1  + n_2 - 1
\end{split}
\end{equation}

式中，$x$为$m_1\times n_1$的矩阵，称为原始数据，$x[i,j]$代表$x$中的第$i$行第$j$列元素。$k$为$m_2 \times n_2$的矩阵，称为卷积核，$k[i, j]$代表$k$中的第$i$行第$j$列元素。$y$为$(m_1 + m_2 -1)\times (n_1 + n_2 -1)$的矩阵，称为卷积结果，$y[i, j]$代表$y$中的第$i$行第$j$列元素。如果从图像上来解释二维离散卷积，卷积层的操作相当于图26所描述的过程。图中，原始图像是一张$5\times 5$像素的数字“4”的二值图像，如果我们定义卷积核为
\begin{equation}
kernel = \left[
\begin{array}{ccc}
~0~&~~~0~~~&~0~\newline
~0~&~~~2~~~&~0~\newline
~0~&~~~0~~~&~0~
\end{array}
\right]\label{equ:kernel}
\end{equation}

<center>![卷积操作](DeepLearningInImageRecognition/image/convlution.png "卷积操作") <br><strong>图26</strong> 卷积操作</center>


那么经过二维离散卷积后，其得到的卷积结果为
\begin{equation}
y = x * kernel = 
\left[
\begin{array}{ccc}
~2~&~~~0~~~&~2~\newline
~2~&~~~2~~~&~2~\newline
~0~&~~~0~~~&~2~
\end{array}
\right]
\end{equation}
将卷积结果再经过一个阶跃函数进行非线性变换后，我们可以看到，卷积层通过式\eqref{equ:kernel}中定义的卷积核对原始图像（即数字4）进行卷积后，其非线性化后的结果依然保留着数字4的特征。由于卷积核是固定的，因此卷积操作经常被认为是一种滤波，即用卷积核去检测特征，将这些特征提取出来。

图26只是利用一个卷积核对原始图片进行卷积得到一张特征图，事实上，正如图25所示，如果我们利用多个卷积核对原始图像进行卷积，那么便可以得到多张特征图。多张特征图，意味着可以提取到原始图像的多个特征，例如在手写数字识别中，我们提取了三张特征图，其中一张特征图表明左上角有一点，一张特征图表明右上角有一个折线，剩下的一张特征图表明右下角有一个点，那么通过这三张特征图，我们就可以判定这个数字是“7”。特征图的作用，在于降低数据的冗余信息，例如“7”这个数字中，横线事实上只需要两个点就可以确定一条直线，竖线也同理只需要两点便可确定一条直线，然而横线与竖线之间存在一个相对位移，因此折线的作用便是刻画相对位移的。

图26中的例子只针对与原始输入数据是一张图像的情况，实际上，卷积操作应该泛化到输入图像为多张的情况。例如，图25中的第二个卷积层，其输入图像便是多张图像。实际中，输入图像也不太可能是一张图像，一张输入图像的情况往往只出现于灰度图像中。然而在彩色图像中，我们知道，彩色图像是具有三张矩阵的，分别代表红（R）、绿（G）、蓝（B）。对于输入图像为多张的情况，解决的方法有两种。一种是利用同一个卷积核去卷积所有的$n$输入图像，将得到的$n$张卷积结果进行相加合并成为一张，在将它进行非线性映射，从而得到一张特征图，这个过程如图27所示。

<center>![使用同一卷积核卷积多张图像](DeepLearningInImageRecognition/image/convlution4featuremap.png "使用同一卷积核卷积多张图像") <br><strong>图27</strong> 使用同一卷积核卷积多张图像</center>


另外一种解决方法是，假设我们有$ m $张输入特征图，而我们想要卷积后得到$ n $ 张输出特征图，那么我们使用 $m \times n$ 个卷积核，令$ k_{i,j}$ 代表从第$ i $张输入特征图映射到第$ j $张输出特征图这个过程中所需要使用的卷积核，$ b_j $代表卷积完成后第$  j $张特征图所要加上的偏置，那么卷积操作就可以描述为：
\begin{equation}
\bigg[\mathcal{M}_1, \mathcal{M}_2, \cdots, \mathcal{M}_m\bigg] \divideontimes \left[
\begin{array}{cccc}
k_{1,1} & k_{1, 2}, & \cdots, & k_{1, n} \newline
k_{2,1} & k_{2, 2}, & \cdots, & k_{2, n} \newline
\vdots &\vdots & \ddots  & \vdots \newline
k_{m,1} & k_{m, 2}, & \cdots, & k_{m, n} \newline
\end{array}
\right ] \boxplus \bigg[b_1, b_2, \cdots, b_n\bigg] = \bigg[\mathbf{M}_1,\mathbf{M}_2, \cdots, \mathbf{M}_n\bigg]
\label{equ:muticonv}
\end{equation}
式中，$\big\lbrace\mathcal{M}_i\big\rbrace_{i=1}^m$为$m$张输入特征图，$\big\lbrace\mathbf{M}_j\big\rbrace_{j=1}^n$为$ n $张输出卷积结果， $\boxplus$为面向元素的加法，$\divideontimes $是我们提出的一种运算，其运算与矩阵乘法类似，唯一不同是在元素操作时，矩阵乘法执行的是乘法操作， 而$\divideontimes $执行的是卷积操作。卷积操作完成后，再进行非线性映射，即可得到多张特征图。式\eqref{equ:muticonv}实际上类似于全连接神经网络的前向传播，但是不同的是，全连接神经网络中，$m \times n$矩阵里的每一个元素代表连接权值，是一个常数，而式\eqref{equ:muticonv}中，$m \times n$矩阵里的每一个元素代表一个卷积核，是一个矩阵。另外一个不同点在于，全连接神经网络执行的是乘法，而式\eqref{equ:muticonv}中执行的是卷积。

事实上，第一种解决方案只是第二中解决方案的特例，在第一种解决方案中，实际上相当于$K_{m \times n}$中的每一列都强制相等，即
\begin{equation}
k_{1, 1} = k_{2, 1} = \cdots = k_{m, 1}
\end{equation}
因此，第一种解决方案意味着更强的正则，或者说更强的惩罚，因为它强制每一列的卷积核都相等。但是我个人认为，尽管这种方法确实能工作得很好，但这是不太合理的。例如在图像中，三个输入图像，也就是RGB三个矩阵，采用第一种方案意味着对三个颜色都同等对待，因为作用在三个矩阵上的卷积核是相同的。但我们直觉上可以感觉到，这三种颜色不应该同等对待，而应区分开来，因此在往后的讨论中，我们只讨论第二种解决方案。

#采样
卷积得到的特征图，需要经过一个采样层，采样层是针对每一张特征图的，即各张特征图的采样时独立互不干扰的，因此采样得到的特征图与原始的特征图之间是一一对应关系。假设我们使用一个均值采样，对于一个$4\times 4$的特征图，我们对其每$2\times 2$区域内取平均，即

\begin{equation}
\left[
\begin{array}{cccc}
1 &~~~~1 &~~~~2& ~~~~2\newline
1 &~~~~1 &~~~~2& ~~~~2\newline
3 &~~~~3 &~~~~4 &~~~~4\newline
3 &~~~~3 &~~~~4 &~~~~4\newline
\end{array}
\right] \rightarrow \left[
\begin{array}{cc}
1&~~2\newline
3&~~4\newline
\end{array}
\right]
\end{equation}

采样层的作用在于压缩数据，使得维度不至于快速增长。想象一个原本为$6\times 6$像素的原始图片，在经过一个$3\times 3$的卷积核进行卷积后，得到的特征图大小为$4\times 4$，但这只是一张特征图，由于在卷积层中我们往往使用多个卷积核进行卷积，假设我们设定卷积层的输出特征图总量为50，那么将会有$50\times 4 \times 4 = 800$个节点，而原来的节点只有$5\times 5 = 25$个节点，这将会使节点增加了32倍。采样层一般都是对卷积得到的特征图进行2倍的缩小，仅此经过采样层后，特征图的大小为$2\times 2$，此时的节点仅为$50\times 2 \times 2 = 200$个。

另一方面，采样层可以抑制位移的变化，卷积得到的特征图，在经过小区域内的平均后，弱化了其绝对位置，而保留了其相对位置，需要注意的是，这里的位移并不仅仅只欧式距离里的位移，还应包括图像的伸缩，旋转等，所以这个位移应理解为广义的位移。

采样的方法除了上面提到的平均采样方案，还有一些别的方案，例如xxx文献中介绍了一种自学习的采样，即小区域内并不是简单的求和取平均，而是类似于加权求和取平均，这些权值便是所需要学习的参数。这两种方案并没有孰劣孰优的说法，实际上两者都能很好的工作，但自学习的方法确实是会比简单的平均采样好一些，但由于平均采样更简单，所以我们往后的讨论只使用平均采样。

#分类器
原始输入数据经过多次卷积采样后，特征图的尺寸不断缩小，最后将使得卷积无法再进行，此时，我们将这些非常小的特征图展开成为一个列向量。例如，一个原始图片为$32\times 32$大小的图像，经过一个$5\times 5$大小的卷积核后得到$28\times 28$的特征图，对其进行均值采样，将变为$14\times 14$大小的特征图，再用$5\times 5$大小的卷积核卷积，将得到$10\times 10$大小的特征图，采样后为$5\times 5$大小，此时再执行一次卷积后，特征图大小为$1\times 1$，这时候再也无法进行采样了，假设现在有100个$1\times 1$大小的特征图，那么它便可以展开成为一个100维的列向量。又例如，一个原始图片为$28\times 28$大小的图像，如果卷积核都设定为$5\times 5$，那么经过卷积、采样、卷积、采样后，将得到$4\times 4$的特征图，此时卷积核尺寸大于特征图的尺寸，卷积无法执行，应将这些特征图展开，假设有10张$4\times 4$的特征图，那么展开后将得到$10 \times 4 \times 4 = 160$维的列向量。

对于最后的列向量，即可以直接使用分类器，也可以在这些列向量的基础上搭建几层隐含层后再使用分类器，这个分类器可以是全连接神经网络或支撑向量机等，选取哪个取决于设计者的意愿。关于分类器如何使用，读者可以参考前面的章节，在卷积网络最顶层的分类器中，与传统神经网络是相同的。

#卷积神经网络的反馈
卷积神经网络的训练方法与传统神经网络的训练方法类似，都是采用反向传播算法，但由于卷积网络特殊的构型，需要对其进行一些改动，但两者的核心都是相同的，即通过后一层的误差注入前一层中，乘上该层激活函数相对于净激活的偏导数后得到该层的误差，利用这个误差乘上净激活相对于输入的偏导数即可得到参数更新的增量。唯一的不同点在于注入的方式不同。

##分类器误差传播
由于卷积神经网络中最顶层与传统的神经网络相同，因此参数校正以及反向传播方式是相同的。有一点需要注意的是，如果网络最后一个卷积层（或采样层）中将特征图拉成一个列向量，那么反向传播的时候需要将列向量还原回特征图形式，例如，如果网络中最后阶段得到10张$4\times 4$大小的特征图，前向传播过程中会将它们合并成为一个160维的列向量，那么在反向传播过程中，需要将160维的误差列向量还原成10张$4\times 4$的特征图形式，此时得到的特征图可以看做是误差特征图。

##采样层误差传播
在采样层中，如果我们使用平均采样，由于平均采样并没有额外的参数需要学习，因此只需要将后一层传播回来的误差继续传播回前一层即可。由于采样层是对前一层局部区域的平均，所以在将误差传播回前一层时，只需要将其尺寸放大到相同的比例，对应的局部区域中每一个元素均取采样层中的元素即可。例如，一个缩小比例为2的采样层，假设它接收到后一层传播回来的误差特征图尺寸为$2\times 2$，那么这个误差传播回采样层的前一层将得到$4\times 4$尺寸的特征图，这个过程如式\eqref{equ:subsampling}所示
\begin{equation}
\left[
\begin{array}{cc}
1&~~2\newline
3&~~4\newline
\end{array}
\right]\rightarrow 
\left[
\begin{array}{cccc}
1 &~~~~1 &~~~~2& ~~~~2\newline
1 &~~~~1 &~~~~2& ~~~~2\newline
3 &~~~~3 &~~~~4 &~~~~4\newline
3 &~~~~3 &~~~~4 &~~~~4\newline
\end{array}
\right] \label{equ:subsampling}
\end{equation}

如果读者在此之前了解过Kronecker积（也称直积），上述过程便是一个Kronecker积过程，即

\begin{equation}
\delta_{conv} = \delta_{sampling} \otimes 1_{n \times n}
\end{equation}
式中需要注意的是，$\otimes$是直积符号而不是逻辑电路里的异或符号。$\delta_{conv}$代表传播回前一层（即卷积层）的误差，$\delta_{sampling} $代表后一层网络传播到采样层的误差，$1_{n \times n}$是一个$n \times n$的单位向量，$n$的取值等于采样层的缩小比例，例如，如果采样层的缩小比例是2，则$n=2$。

##卷积层误差传播
与传统的全连接神经网络类似，卷积层接收到后一层传播回来的误差后，需要乘以当前层激活函数相对于净激活的偏导数，得到当前层的误差，即
\begin{equation}
\delta^\ell_i = \delta^{\ell + 1}_i \cdot \frac{\partial f(net_i)}{\partial net_i}
\end{equation}
由于卷积网络中有多张特征图，所以$\delta^\ell_i $代表当前层（$\ell$层）的第$i$张误差特征图，$\delta^{\ell + 1}_i$代表第$\ell + 1$层传播回来的第$i$张误差特征图，$net_i$代表第$i$张特征图的净激活。

计算得到当前层的误差后，通过卷积的自相关性，利用这个误差可以计算卷积核以及偏置的迭代增量，即
\begin{equation}
\frac{\partial J}{\partial k_{i, j}^\ell} =rot180\bigg(conv\Big(x_i^{\ell-1}, rot180(\delta_j^\ell),'valid' \Big)\bigg) 
\end{equation}
式中，$rot180( \cdot )$执行将一个矩阵旋转$180^\circ$操作，其目的在于利用卷积的自相关性质，conv为卷积操作，‘valid’代表卷积操作范围限制在可用区域内。对于偏置，其梯度为
\begin{equation}
\frac{\partial J}{\partial b_j} = \sum\limits_{u, v} (\delta_j^\ell)_{uv}
\end{equation}
获取参数的梯度后，对卷积层的参数进行更新，随后将卷积层的误差反向传播到采样层，其公式为
\begin{equation}
\delta_j^{\ell -1} = f'(u_j^\ell) \boxdot conv\bigg(\delta_j^\ell, rot180\Big(\sum\limits_{i\in M_j^\ell} k_{ij}^\ell\Big), 'full' \bigg)
\end{equation}
式中，$\boxdot$为面向元素的乘法，‘full’代表卷积的操作范围是全图卷积。通过以上策略，对网络进行类似的反向传播，即可对整个网络进行反馈校正。


#GPU计算
上世纪六十年代提出的摩尔定律到目前为止已经持续了半个多世纪，硅技术似乎已经难以再有重大突破，摩尔定律在未来几年或将成为过去。然而当前计算机的计算能力仍不足以满足人们的需求，并行技术的发展在一定程度上缓解了这种压力，某种程度上而言，计算并行化可以看做是摩尔定律的一种延伸。

GPU（Graphic Processing Unit）又称“图形处理器”，是相对于CPU的一个概念，其最初目的是满足计算机图形界面中人们对于实时、高清的三维图形的需求。在图形开发中，由于图形渲染及变换等操作是带有可并行特征的，因此对于GPU的设计者而言，他们更倾向于添加更多的核心而不是提高核心的运行效率，通过多个核心以及线程技术，使得同一条指令可在每个元素上执行。此外，他们还取消了CPU中的缓存与逻辑控制部件，因此GPU适用于计算密集的并行计算，而CPU更适用于含有复杂流控的计算。

但是最初的GPU是为图形开发者而开发的平台，对于非图形开发者而言，使用GPU进行通用计算并不是一件容易的事。为此，ATI公司（已被AMD收购）于2005年提出的ATI Stream方案，NVIDIA公司在2007年推出的CUDA平台，都是为了解决GPU通用计算问题而做出的努力。在GPU通用计算不断发展的同时，新的规范也被不断地提出，Apple公司在2008年提出OpenCL（Open Computing Language）规范，微软提出的DirectCopmute规范，其目的都在于制定了一套API，并在此基础上开发GPU通用计算软件。

在这些GPGPU（General Purpose GPU）方案中，由于CUDA为开发者提供了一个类似于C的编程环境，使用者可以快速学习，所以受到了广泛的使用。

##GPU体系结构
相比于CPU而言，GPU由于其设计原则就是针对密集运算的，所以在浮点运算上占着先天优势。近几年CPU在运算效率上的提升缓慢，与此同时，GPU计算却飞速发展，其运算性能已远远超过CPU。如图所示是Intel的CPU与NVIDIA的GPU在各个型号上每秒浮点运算量的对比。相比于CPU而言，GPU由于其设计原则就是针对密集运算的，所以在浮点运算上占着先天优势。近几年CPU在运算效率上的提升缓慢，与此同时，GPU计算却飞速发展，其运算性能已远远超过CPU。如图28所示是Intel的CPU与NVIDIA的GPU在各个型号上每秒浮点运算量的对比\footnote{图片出自于NVIDIA的官方技术文档《CUDA C Programming Guide》}。



<center>![GPU与CPU在每秒浮点运算量上的差异](DeepLearningInImageRecognition/image/GPUvsCPU.png "GPU与CPU在每秒浮点运算量上的差异") <br><strong>图28</strong> GPU与CPU在每秒浮点运算量上的差异</center>

由于GPU中取消了逻辑控制单元，相比于CPU其体系结构有着很大的不同。典型的CPU结构带有三级缓存，数据由内存经过三层缓存后才进入到处理器核心，这个结构如图所示。GPU同样带有缓存，这个缓存一般只有两级，与CPU不同的是，CPU中只有一个处理器，而GPU中并没有处理器核心的概念，取而代之的是流处理器簇（Streaming Muntiprocessor），在一个GPU中往往含有多个流处理器簇，尽管它们与CPU处理器核心有着很大的差异，但某种程度上也可以看做是GPU的核心，整个GPU的结构如图29所示。


<center>![CPU结构](DeepLearningInImageRecognition/image/CPU.png "CPU结构") ![GPU结构](DeepLearningInImageRecognition/image/GPU.png "GPU结构")<br><strong>图29 </strong>CPU与GPU结构差异</center>


CPU为了实现多核技术，往往在一个芯片中集成多个CPU核心，例如在Intel i7处理器中含有4个CPU核心，多核心使得CPU可以并行执行计算，但相比于GPU而言，CPU的并行粒度是非常大的。例如要将一个含有100个元素的向量的每一个元素乘上一个常数2，那么对于4核的CPU，我们可以指派1号CPU执行第1$\sim$25个元素的操作，2号CPU执行第26$\sim$50个元素的操作，但对于GPU而言，它可以直接开辟100个线程，每个线程针对每个元素进行操作，这些线程是并行线程而不是并发线程，因此GPU可以实现小粒度的并行。

GPU只所以能开辟大规模线程是因为一个GPU包含了一个流处理器簇阵列，这个阵列由多个流处理器簇构成，例如费米架构的GPU的阵列大小为16。而每个流处理器簇又包含了几十个到几百个的CUDA核心，例如，采用开普勒架构的GPU每个流处理器簇包含48个CUDA核心，而采用费米架构的GPU每个流处理器簇包含192个CUDA核心。这些核心并不类似于CPU的核心，CPU的每个核心只能执行一个线程，而CUDA核心可以并行执行多个线程。

GPU的线程由线程网格管理，线程网格可以看做是一个二维网格，这个结构如图30所示。在这个网格中，一个维度是线程块，另一个是线程束。每个GPU核心最多可包含65536个线程块，每个线程块最多可包含512个线程束，这意味着我们可以一次开辟最多大约3300万个线程，目前的费米架构已经实现每个线程块可包含1024个线程束，因此它最多可开辟6600万个线程。但这只是说我们可以在代码中开辟线程，并不意味着执行线程也是这个数量级。事实上，每个流处理器簇可执行的线程数量是有限制的，这个数量级大约是一千左右。

<center>![线程网格](DeepLearningInImageRecognition/image/threadGrid.png "线程网格") <br><strong>图30</strong> 线程网格</center>


实际中在跑的线程数大约为几万，然而我们却可以在代码中开辟几千万的线程，这得益于GPU对硬件的隐藏机制，类似于操作系统的虚拟地址，GPU会自动地将这几千万的虚拟线程在几万实际线程中调度，而程序员不需要参与到这个过程中，只需要在代码中开辟线程即可。这个机制使得硬件升级扩展变得简单，因为虚拟的线程与实际调度的线程是分离的，GPU为我们自动调度，我们可以随意的更换未来更多核心的GPU而不需要改动我们的代码。

为了更好地理解线程块与线程的概念，我们举一个GPU中实现两个向量相加的例子，如下所示

<pre><code class="c">
__kernel__ void add(int *c, int *a, int *b){
	int tid = blockId.x;
	c[tid] = a[tid] + b[tid];
} 
</code></pre>

代码8.1中的的\_\_kernel\_ \_ 代表这是一个在GPU中执行的代码，我们称其为内核函数。由\_\_kernel\_\_ 标记的代码将由nvcc编译器编译，而没有这个标记的函数将由C++的编译器编译\footnote{例如Windows操作系统下的msvc或Linux操作系统下的gcc}。第2行代表获取当前的线程号，这里我们假定线程号就是线程块的编号，即默认每个线程块只有一个线程在运行。如果每个线程块有多个个线程在执行，那么第2行代码应改为

<pre><code class="c">
int tid = threadIdx.x + blockId.x + blockDim.x;
</code></pre>

观察图30，这实质上类似于二维索引空间转换为线性空间的代码。第3行代表每个线程执行一个操作，即将向量a中的第tid个元素与向量b中的第tid个元素相加，并存储在向量c的第tid个元素中。这可以理解为，代码会做为一个副本分发给各个线程，各个线程拿到这段代码后，根据自己的线程ID（即tid）执行向量a和向量b中的第tid的元素的操作。

##CUDA
CUDA（Compute Unified Device Architecture）是NVIDIA公司在2007年推出的高性能运算平台，它可以让GPU在执行常规的图形渲染的基础上额外地实现高性能的通用并行计算。CUDA包含了CUDA指令集架构以及GPU内部的并行计算引擎，通过利用 GPU 的处理能力，可大幅提升计算性能。支持CUDA平台的GPU包括NVIDIA Tesla 、NVIDIA Quadro 以及NVIDIA GeForce多个系列，其价格也涵盖了高端到底端多个市场，使得CUDA能够满足从消费级到专业级等多个方面的需求。目前为止， CUDA已经应用到图像与视频处理、计算生物学、流体力学模拟、金融风险分析、地震分析等多个领域，全球五百强企业以安装700多个基于CUDA的GPU集群，这些公司包括了能源领域的斯伦贝谢与雪佛龙以及银行业的法国巴黎银行等。

在CUDA中，程序员需要手工将数据从内存中迁移到GPU中，还需要负责GPU内存的回收，例如，为了执行两个向量的加法，其片段如下所示
<pre><code class="c">
int a[N], b[N], c[N];
int *dev_a, *dev_b, *dev_c;
//init a[N], b[N].....
cudaMalloc((void**)&dev_a, N*sizeof(int));
cudaMalloc((void**)&dev_b, N*sizeof(int));
cudaMalloc((void**)&dev_c, N*sizeof(int));
cudaMemcpy(dev_a, a, N*sizeof(int),cudaMemcpyHostToDevice);
cudaMemcpy(dev_b, b, N*sizeof(int),cudaMemcpyHostToDevice);
add<<<N, 1>>>(dev_c, dev_a, dev_a);	
cudaMemcpy(c, dev_c, N*sizeof(int),cudaMemcpyDeviceToHost);
cudaFree(dev_a);
cudaFree(dev_b);
cudaFree(dev_c);
</code></pre>

在代码中，我们先在GPU中申请内存，即对应的4$\sim$6行，随后在7$\sim$8行中将内存中的数据迁移到之前申请的GPU内存中。第9行执行代码8.1实现的加法内核函数，在GPU中开辟N个线程块，每个线程块含有1个线程，GPU完成计算后，我们在第10行将计算结果从GPU中迁移回内存，最后第11$\sim$13行释放之前申请的内存。释放内存是重要的，如果申请了内存不释放便会导致内存泄露，当内存消耗完毕后程序崩溃。

我们不由感叹，为了执行一个简单的向量加法就要编写如此多的代码，我们需要手工申请内存，手工将数据迁移到GPU中，手工调用内核函数，调用完毕后需要手工将计算结果从GPU中迁移回来，最后还需要手工释放申请的内存。如果用户不是专业的程序员，那么代码编写的过程十分困难。因此，在CUDA之上有多个团队为机器学习研究人员开发了专门的第三方库，我们将会介绍几个常见的包。

##Cudamat
Cudamat是一个由多伦多大学开发的一套针对于Python的开源第三方库\citeup{cudamat}，它基于CUDA，在实现GPU高性能计算的同时保留了Python“语法优雅”的特性，所以使用者可以很方便地在Python语法层次上调用矩阵运算库。开发Cudamat的目的是为了方便机器学习建模，使科研人员从繁琐的CUDA编程中解放出来，由于GPU在浮点并行运算上巨大的优势，所以在计算密集的矩阵运算任务中Cudamat相对于numpy或MATLAB，其运算速度大约提升了50倍左右。

在Cudamat中，开发者已为我们重载了一些运算符，这使得矩阵的四则运算运算以及面向元素的四则运算，以及矩阵的切片、转置等操作不再需要编写大量的代码或调用对应的函数。此外，开发者还提供了一些常用的函数，例如面向元素的exp()、log()、sqrt()、pow()，矩阵的乘法以及面向轴的求和、随机矩阵的生成等。例如，为了实现一个logistic函数，只需要在Python中只书写如下语句

<pre><code class="python">
def logistic(A):
   expTerm = cudamat.CUDAMatrix(numpy.random.randn(A.shape))
   cm.exp(-A, target=expTerm)
   return 1 / (1 + expTerm)
</code></pre>


尽管Cudamat并没有将CUDA的所有功能都囊括其中，但在机器学习中常用的功能基本都实现了，所有我们可以在不需要了解底层CUDA的前提下高效地建立数学模型的代码，减轻了我们的工作量。

##Gnumpy
在Python科学计算中，numpy与scipy两个第三方包充当着重要角色，其中numpy凭借其优美的语法实现以及高效地执行速率深受人们喜爱。在numpy中，有着许多巧妙的设计，比如广播特性、切片、方便的元素存取、丰富的函数等。其语法特性与MATLAB接近，几乎MATLAB上能实现的功能在numpy中都能找到对应的实现，此外还加入一些MATLAB所不支持的功能，例如方便地嵌入C++代码、方便地存储图像、网络IO等功能。尽管numpy语法简单，运行效率接近于C，但由于其本质上还是基于CPU的运算，所以在大规模的计算中运行效率显得有些难尽人意。

在Cudamat上编写代码要比直接地使用CUDA编写代码要方便得多，我们不再需要了解底层，不再需要担心GPU的内存释放，不再需要编写复杂的内核函数，然而，Cudamat代码要比numpy代码逊色不少，例如代码8.3中的exp函数需要在参数列表中带上返回变量，而这个返回变量又必须要先声明，无法实现变量的动态使用，所以Cudamat带着明显的C语言风格，这违背了Python关于“简单就是美”的设计原则。鉴于以上原因，多伦多大学在cudamat的基础上开发了新一代的开源第三方包---Gnumpy\citeup{gnumpy}。Gnumpy其计算本质是GPU计算，但其接口特性接近于numpy。尽管Gnumpy是基于Cudamat的，但在Gnumpy中你将看不到Cudamat的影子，开发者已经将其隐藏了，你看到的只有类似于numpy那样便捷的接口	。例如，同样是实现logistic函数，在Gnumpy中只需写成代码8.4中的形式

<pre><code class="python">
def logistic(A):
   return 1 / (1 + gnumpy.exp(-A))
</code></pre>

事实上，gnumpy已经为我们实现了logistic函数，因此我们只需要一条语句即可完成该功能

<pre><code class="python">
A.logistic()
</code></pre>


使用Gnumpy更容易编写程序，代码相对于Cudamat而言更简短，也更容易阅读与调试，对于拥有numpy使用经验的开发者而言可以很容易地上手。尽管Gnumpy是基于Cudamat的基础上进行的二次开发，但其运行效率接近于Cudamat，因此使用者无需过于担心效率问题。


##PyCUDA
无论是Gnumpy或是Cudamat都只提供了一些矩阵的基本操作，我们无法实现一些这两个库没有的矩阵操作，例如二维离散卷积。如果我们因为内存管理的原因不想直接写繁琐的CUDA C代码，那么PyCUDA是一个可以选择的库。PyCUDA是由Andreas Klockner与Nicolas Pinto等人开发的一个Python第三方库\citeup{kloeckner_pycuda_2012}，其目的在于允许我们在Python中内嵌CUDA C代码。在PyCUDA中，我们可以只书写内核函数，而不写内存管理的代码。在程序第一次执行时，Python会调用CUDA的编译器将CUDA C的代码编译成动态链接文件，编译完成后可以直接在Python中调用这个函数。例如，为了实现一个矩阵相乘的函数，我们的代码如下所示

<pre><code class="python">
import pycuda.driver as GPU
from pycuda.compiler import SourceModule
def add(A, B, N):
    code = SourceModule('''
       __global__ void add(int *c, int *a, int *b){
          int tid = blockId.x;
          c[tid] = a[tid] + b[tid];
       }
    ''')
    addByGPU = code.get_function("add")
    C = numpy.zeros_like(A)
    addByGPU(GPU.Out(C), GPU.In(A), GPU.In(B),
             block=(N, 1, 1), grid=(1, 1))
    return C
</code></pre>

代码的第4$\sim$9行通过字符串的形式嵌入CUDA C的内核函数，第10行试图去获取名为“add”的内核函数，如果这行语句是第一次执行，并且在我们已经通过字符串形式嵌入了“add”这个函数，那么Python就会调用nvcc编译器对代码进行编译，并保存为动态链接文件，当下一次再试图获取这个内核函数时不需要再编译一次而直接调用。第$12$行执行GPU中的计算，以A、B作为输入，C作为输出，执行在N个线程块上。最后返回运算结果C。

PyCUDA使得我们的代码自由度变得更高，我们可以实现任何一个我们想要的内核函数。但与此同时它也使得我们的代码变得复杂。天下没有免费的午餐，选择一个自由度高的库或是选择一个代码简单的库完全取决于你的权衡。

##Caffe
以上的几个Python第三方库都是一些机器学习中的通用库，这些库只提供基础的功能，利用他们可以实现很多算法。如果一个科研人员没有太多程序设计的经验，而又希望将他设计的神经网络在计算机上实现，那么Caffe是一个选择。Caffe是由加州大学伯克利分校的Jia Yangqing 等人的领导下开发的一套基于CUDA的深度学习工具箱\citeup{jia2014caffe}，其源代码由C++/CUDA实现，在此之上提供了Python、MATLAB接口，并且可以通过命令行执行。在Caffe中，开发者已经编写好各种各样的网络层的代码，如全连接层、卷积层等。使用者无需编写具体的代码，Caffe让深度学习的研究人员从具体的代码中解放出来，我们只需要将自己设计的网络模型写成配置文件即可。如下是一个神经网络的配置文件中的一个片段

<pre><code class="javascript">
layers {
    name: "pool1"
    type: POOLING
    bottom: "conv1"
    top: "pool1"
    pooling_param {
        pool: MAX
        kernel_size: 3
        stride: 2
    }
}
</code></pre>

在配置文件片段中，定义了一个池化层。配置文件由两部分组成，2$\sim$5行为属性定义，6$\sim$10行为参数定义。其中第2行定义了这层的名字，第3行定义了层的类型，第4行定义了这层网络的前一层网络的名字，第5行定义了后一层网络的名字（这里就是它自身）。第7行定义了这层池化层使用的是最大池采样，第8行定义了卷积核的尺寸为$3\times 3$，第9行定义了卷积间隔为2。


#实验现象及讨论
我们在MNIST数据集上分别实现了深度置信网络与卷积神经网络，使用深度置信网络训练得到的模型实现了98.72% 的识别正确率，使用卷积神经网络实现了98.9%的识别正确率。我们在CIFAR-10数据集上实现一个卷积神经网络，实现了62%的正确率，此外，通过Caffe测试了由xxx提出的网络构型的学习效果，并将其与我们的网络学习效果进行对比。
##数据集简介
MNIST与CIFAR-10是学术界两个重要的数据集，这两个数据集一般作为标准数据集而存在，每当人们提出一种新的算法，都会用这两个数据集做验证，下面我们将简单介绍这两个数据集。
###MNIST
MNIST数据集是一个真实世界中采集的手写数字图像数据集\citeup{lecun2010mnist}，它由NIST会议收集并持有，读者可到MNIST主页免费获取该数据集。这个数据集一共含有4个文件，分别存储训练数据、训练标签、测试数据、测试标签。文件以二进制文件形式存储，不过我们可以很容易编写一段小代码将其转换成图像。训练集共含有60000个样本，测试集含有10000个样本，这些样本收集自500位不同的人的手写字体。


<center>![MNIST数据集部分数据样本](DeepLearningInImageRecognition/image/MNIST.png "MNIST数据集部分数据样本") <br><strong>图31</strong> MNIST数据集部分数据样本</center>


每个数据样本是$28\times 28$像素的灰度图像，由于引入了抗锯齿效果，所以图像数值范围是$0\sim 255$而不是二值图像。图像已经经过预处理，因此图像会集中在中心$20\times 20$的区域内，此外，图像的中心点与像素点的重心重合，所以如果要使用模板匹配的方法（比如k近邻，SVM等）进行分类的话对图像再进行一些预处理使得数字的几何中心与图像中心重合会改善你的算法性能。

如图31是MNIST数据集中的一小部分样本的展示，原始的数据应该是黑底白字的，为了美观，我们将其颜色反转并加上周围的边框。

###CIFAR-10
CIFAR是一个由Alex Krizhevsky, Vinod Nair以及Geoffrey Hinton收集的一个含有8千万张图片的数据集，这些图片并没有经过手工标注。而CIFAR-10是这个数据集的一个子集，含有50000个训练样本和10000个测试样本，这些样本经过人手工标注为10个类别，分别是飞机、小汽车、鸟、猫等。读者可以从CIFAR-10的官网免费获取这个数据集，它包含7个文件，其中有5个文件是训练集，每个文件包含10000个训练样本，有1个文件存储测试集，包含10000个样本，这些样本都被随机打散，所以不用担心类别的出现顺序会导致算法性能上的差异。剩余的一个文件是标签值与类别名字的键值对。CIFAR-10为我们提供了三种存储形式，分别对应Python、MATLAB与二进制形式的数据存储格式，读者可根据自己的语言背景选取其中一种进行下载。

<center>![CIFAR-10数据集部分数据样本](DeepLearningInImageRecognition/image/CIFAR-10.png "CIFAR-10数据集部分数据样本") <br><strong>图32</strong> CIFAR-10数据集部分数据样本</center>

每个数据样本都是大小为$32\times 32$的彩色图像，因此每张图像应包含三张$32\times 32$大小的矩阵，分别代表R、G、B三个原色通道。如图32所示是这个数据集的一部分样本，我们可以看到，这些图像更接近于真实生活中的图像，相比于MNIST而言，每个类别个体的图像差异较大，而不像MNIST中每个类别的个体差异较小，所以在CIFAR-10数据集中使用模板匹配的方法进行分类是几乎不可能的。

##深度置信网络在MNIST数据集上的性能
在MNIST数据集上，我们设计了一个7层神经网络，每层所含的节点分别是784、621、982、600、410、569、10，最底层的节点数是根据原始数据输入维度决定的，即$28\times 28 = 784$，最顶层的节点数是根据最终的类别决定的，即10个类别。中间的隐含层节点我们随意选取，这些节点是如此的随意以至于源自我的银行卡号。在深度置信网络中，对隐含节点并没有过多的要求，大致合理即可。

整个网络可以看做5个受限玻尔兹曼机叠加组成，分别是784$\sim$621，621$\sim$982，$\cdots$，410$\sim$569，最后一层569$\sim$10是softmax分类器。在整个网络的训练过程中，我们先依次对其中的5个受限玻尔兹曼机做贪婪训练，即先训练784$\sim$621的受限玻尔兹曼机，训练完毕后将所有的样本（60000个）通过这个训练完毕的受限玻尔兹曼机前向传播，得到60000个621维的数据样本，用这些维度变换后的样本训练下一个，即621$\sim$982的受限玻尔兹曼机，以此类推。最后的softmax分类器其预训练是将其当做一个两层softmax网络进行预训练。

观察受限玻尔兹曼机的权值更新公式\eqref{equ:MAMAMA}、\eqref{equ:MBMBMB}以及\eqref{equ:MCMCMC}，为了方便大家观察，我们将这三个公式再一次书写一次

\begin{equation}
\frac{\partial\ln P(v)}{\partial w_{i, j}} \approx
 P(h_i = 1 | v^{(0)})v_j^{(0)} - P(h_i = 1 | v^{(k)})v_j^{(k)}
\end{equation}

\begin{equation}
\frac{\partial\ln P(v)}{\partial b_{vi}} \approx
v_j^{(0)} - v_j^{(k)}
\end{equation}

\begin{equation}
\frac{\partial\ln P(v)}{\partial b_{i}} \approx
 P(h_i = 1 | v^{(0)}) - P(h_i = 1 | v^{(k)})
\end{equation}


这三个公式背后隐藏着一层重构的含义，即对于一个两层的受限玻尔兹曼机，在第一层的数据通过前向传播得到第二层的数据，第二层的数据反向注入得到第一层的数据，数据经过这样一个迁移，相当于利用提取的特征重构原始样本，因此在受限玻尔兹曼机的训练过程中，一个刻画其训练情况的方法是跟踪其重构误差，如图33所示是某一层受限玻尔兹曼机的重构误差下降曲线。

<center>![受限玻尔兹曼机对数字的重构](DeepLearningInImageRecognition/image/reconstructImage.png "受限玻尔兹曼机对数字的重构") <br><strong>图33</strong> 受限玻尔兹曼机对数字的重构</center>



最顶层的softmax分类器的训练也是贪婪的，即它只训练569$\sim$10两层网络之间的参数，在这里，训练周期我们不建议太长，一般训练5$\sim$10个周期即可，否则在随后的方向传播过程中，如果softmax预训练过久，则网络的输出误差较小，没有误差就难以进行反向传播，全局微调容易失败，这会导致网络陷入局部最优解，这个局部最优由最顶层的softmax决定而不是整个网络决定。

当整个网络预训练完毕后，我们执行全局的反向传播算法对参数进行微调，这个过程与传统的神经网络相同，我们不进行过多的叙述，如图34所示是整个网络进行反向传播时的误差下降曲线

<center>![深度置信网络误差下降曲线](DeepLearningInImageRecognition/image/DBNTrainingErrorAndTestError.jpg "深度置信网络误差下降曲线") <br><strong>图34</strong> 深度置信网络误差下降曲线</center>


网络训练完毕后，我们选取了一部分网络识别错误的数字，将其展示在图35中，每个样本下边的黑色数字代表测试集给定的标签，而红色数字代表网络的预测标签。我们可以发现，这些错误的样本中，有一部分自身就带有二义性，人也难以区分究竟是哪个数字，而有一部分样本人可以很容易识别，网络却识别错误，还有一部分样本数据本来就是错误的，根本无法识别它是哪个数字，这时候我们不能舍弃机器也能将其识别出来。

<center>![被网络误分类的样本](DeepLearningInImageRecognition/image/errorClassify.png "被网络误分类的样本") <br><strong>图35</strong> 被网络误分类的样本</center>

在整个网络的训练中，我们使用了动量项、权衰减技术，而没有没有使用降维技术，因为数据维度并不是特别高，计算机的处理能力足以应付。如果原始数据的维度非常高，比如几百万维，那么就需要采用一些降维技术将原始数据进行压缩。

深度置信网络在一定程度上仍然带有模板匹配的气息，因为我们如果只使用2000个样本作为训练集而不是全部的60000个样本，网络也能实现90多的正确率，后面中的实验中我们会看到，这种策略在卷积神经网络中是行不通的。


##卷积神经网络在MNIST数据集上的性能
在MNIST数据集，我们设计了一个6层卷积网络，其网络构型描述如下

1.1张$28\times 28$的原始图像

2.卷积原始图像得到6张$24\times 24$特征图

3.对6张特征图进行采样得到6张$12\times 12$特征图

4.对6张特征图进行卷积得到12张$8\times 8$特征图

5.对12张特征图进行采样得到12张$4\times 4$特征图

6.此时12张$4\times 4$特征图无法再进行卷积，将其展开得到192个节点

7.192个节点与10个输出节点做全连接网络，与传统神经网络一样


其中，激活函数我们选取的是sigmoid函数，当然这个函数也可以换成ReLU函数，全连接网络我们采用平方误差作为准则，而不是深度置信网络中的softmax分类器。在这个网络中，我们不采用预训练而是直接进行全局的反向传播。以上的网络构型的选取方案都是随意的，并没有说一定要采用这个方案。

实验获取的训练误差及测试误差曲线如图36所示，训练完毕后，我们在MNIST上取得了98.9%的正确率。我们可以看到，在网络训练的前20个周期，训练误差与测试误差迅速下降，随后的周期中误差缓慢下降，到了后期，收敛十分缓慢，但依然会有下降的趋势。有意思的是，对网络训练一个很长的周期并不会产生明显的过学习现象，所以如果你需要实现一个高识别率的网络，那么你可以放心地等待一段很长的的时间。

<center>![卷积神经网络训练误差及测试误差](DeepLearningInImageRecognition/image/CNNTrainingErrorAndTestError.png "卷积神经网络训练误差及测试误差") <br><strong>图36</strong> 卷积神经网络训练误差及测试误差</center>

值得注意的是，误差下降过程带有明显的波动性，在深度置信网络的训练过程中，一般到了训练的后期，识别率不会有太大的波动，比如，深度置信网络在到达98.70%的正确率后，其波动范围就在98.70%附近波动，可能是98.73%、98.74%。然而，在卷积网络中，到达98.70\%后，它可能一下子跌到98.40%，然后又升到98.80%，这种较大范围的波动，应该不是随机梯度造成的，因为深度置信网络中我们采取随机梯度更新时也没有这么大的波动，我们推测这是因为卷积网络代表着一种非常强的惩罚（强迫权值共享），惩罚过大导致波动变大。

在实验中，我们并没有采用权衰减，因为我们发现使用权衰减后网络的性能变差。此外，我们发现当改变网络中的一些参数，比如特征图的张数，学习率时，对网络的收敛影响较大，但对最终结果并没有太大影响。卷积网络对样本的需求量非常大，实验中，我们选取2000个样本作为训练集对网络进行训练，网络完全不会收敛，这与深度置信网络是不一样的，只有我们将所有的60000个样本作为训练集对网络进行训练时，网络才开始收敛。我们估计这是因为卷积网络的权值共享导致它只有通过大量的样本才能学习特征，这与模板匹配方法有着很大的区别。

网络训练完毕后，我们对测试集中的一部分数据进行观察，第一层卷积层提取出的特征如图37所示。我们分别选取了$0\sim 9$一共10个样本，每一行代表一个样本。其中，每一行的第一张是原始的$28\times 28$图像，随后六张是卷积出来的六张$24\times 24$大小的特征图。观察图37，我们可以发现一些有意思的现象。例如，原始图像是黑底白字的，而有一些特征图反转成为白底黑字，又比如，第六张特征图是对图像进行边界检测，为了验证我们这个想法，我们随机选取了“4”这个数字的几个样本进行特征抽取，其结果如图37 显示，通过观察，我们不难发现，对于不同的写法，其提取到的特征都是近似的，它会检测“4”的左边竖线的上方一点以及对下来的一个折线，右边竖线的上方一点以及下方的一点。另一个有意思的现象是，第三张特征图看起来是一个3D图像，想象图像的左上角有一束阳光洒下，当我们伸出右手，掌心贴着当前的纸张页面，大拇指朝纸张左方，握拳，数字经过我们四个手指的方向旋转过一定角度后，那么阳光洒下的阴影如同第三张特征图所示。这个现象在第五张特征图中也出现了，只是第五张特征图的阳光处于左侧而不是左上角。同样伸出我们的右手，掌心贴着当前的纸张页面，大拇指朝纸张下方，握拳，我们可以看到数字经过我们四个手指的方向旋转过一定角度后，阳光洒下的投影正如第五张特征图所示。


<center>![针对0-9不同数字提取到的特征图像](DeepLearningInImageRecognition/image/CNNFeatureMaps.png "针对0-9不同数字提取到的特征图像") ![针对数字“4”提取到的特征](DeepLearningInImageRecognition/image/fourNumber.png "针对数字“4”提取到的特征")<br><strong>图37 </strong>第一层卷积层抽取得到的特征图</center>

##卷积神经网络在CIFAR-10数据集上的性能
相比于MNIST数据集，CIFAR-10数据集的识别更为困难。由于计算资源的限制，我们只在CIFAR-10上设计了一个较小的卷积网络，与MNIST手写数字的卷积网络构型类似，在CIFAR-10数据集上，我们同样设计了一个4层卷积网络，其网络构型描述如下

1.3张$32\times 32$的原始图像

2.卷积原始图像得到9张$28\times 28$特征图

3.对9张特征图进行采样得到9张$14\times 14$特征图

4.尽管9张$5\times 5$特征图仍然可以被卷积，但我们依然将其展开为1764个节点

5.1764个节点与10个输出节点做全连接网络，与传统神经网络一样

网络的属性与MNIST实验中的相同，激活函数我们依然选取sigmoid函数，全连接网络依然采用平方误差作为准则，对网络进行训练得到训练集误差下降如图38左图所示，测试集误差量下降如图38右图所示。需要注意的是，看起来在左图误差下降速度非常快，对比右图，其斜率更大，然而这是一个假象，因为我们对纵轴进行了尺度缩放，事实上在CIFAR中误差下降的非常慢，而且在训练集与测试集中仍然后很大的误差可以下降。

<center>![训练误差下降曲线](DeepLearningInImageRecognition/image/CIFARtrainError.png "训练误差下降曲线") ![测试误差下降曲线](DeepLearningInImageRecognition/image/CIFARtestError.png "测试误差下降曲线")<br><strong>图38 </strong>CIFAR的训练误差与测试误差</center>


因为CIFAR-10数据集的复杂性，本应该建立一个庞大的网络进行训练，但由于我们的计算资源有限，时间紧迫，所以无法实现一个更大的卷积网络，此外，对网络的训练我们也仅仅训练了400个周期左右，因此，整个网络训练完毕后我们只得到62%的识别正确率。

如图39所示是一部分被网络正确识别的样本，其中每一行代表一个类别，图中总共包含了10个类别100个样本。观察这些样本我们会发现，网络能识别的图像对位移、旋转等性质具有不敏感性。例如，在飞机这个类别中，网络可以识别头部向左、向右等多个角度的飞机，还可以识别俯仰角不同的图片，由于这些图片不具备模板性，所以卷积网络基本没有了模板匹配的缺点。



<center>![被网络正确识别的CIFAR-10部分样本](DeepLearningInImageRecognition/image/CIFARcorrectClassfy.png "被网络正确识别的CIFAR-10部分样本") <br><strong>图39</strong> 被网络正确识别的CIFAR-10部分样本</center>



我们跟踪了网络无法识别的样本，将其一部分绘制如图40所示。图中每个样本下方的黑色数字代表由训练集提供的标签值，而红色数字代表网络的输出标签值，标签值于类别名字的键值对可参照图32。我们发现，在一些样本中，网络会将大卡车错误地识别成小汽车或将小汽车错误地识别成大卡车，这似乎可以原谅，但有一些图像的错误识别是我们无法原谅的，例如将马识别成大卡车。这些错误的样本中很多样本人是可识别的，而机器不可识别，我们推测这是因为我们的网络设计得不够庞大，训练周期也不长，导致网络无法进行更好的特征提取，从而影响最终的识别效果。

<center>![被网络错误识别的CIFAR-10部分样本](DeepLearningInImageRecognition/image/CIFARerrorClassfy.png "被网络错误识别的CIFAR-10部分样本") <br><strong>图39</strong> 被网络错误识别的CIFAR-10部分样本</center>



为了描述网络的特征提取性能，如同在MNIST上卷积网络的工作，我们同样将第一层卷积层提取到的特征绘制如图40所示。我们选取了“飞机”类别下的9个样本，每一行代表一个样本。其中，每一行的前三张黑白图像是原始$32\times 32$大小的RGB通道，这三张图像合成第四张$32\times 32$彩色图像。随后的九张是第一层卷积层提取到的九张$28\times 28$大小的特征图。对比这些原始数据与特征图，我们发现，原始数据中图像是含有冗余的，大部分的特征图过滤掉这些冗余信息，将飞机的边界提取出来形成特征图。这些特征图中，有一些特征例如第2张，第8张并没有提取到一些人可理解的特征，我们猜测随着训练周期的增加，这些特征将会逐渐显露出来，由于时间有限，我们并没有验证我们的猜想。

<center>![针对“飞机”类别提取的特征](DeepLearningInImageRecognition/image/CIFARfeatureMap.png "针对“飞机”类别提取的特征") <br><strong>图40</strong> 针对“飞机”类别提取的特征</center>

这些特征图应该可以通过选取某几张组成彩色的特征图，但我们并不知道选取哪几张合适，所以我们并没有做这一步工作。此外，这些特征图表明，在他们之上应该再添加一些卷积层对特征继续提取，而不是我们设计的全连接网络，由于我们的计算资源十分匮乏，所以我们也没有进一步展开这项工作。

##使用Caffe实现的CIFAR-10数据集训练
目前学术界认为CIFAR-10数据集已被解决，因为最好的识别效果由xxx实现，正确率为91\%。另一识别率较高的网络由Alex Krizhevsky等人实现，其识别率为89\%，这个网络稍微有点复杂所以我们不会在本文中提及，更多的讨论可阅读其论文xxxx。在Caffe中的卷积网络构型采取的是Alex Krizhevsky的方案，为了实现对比，我们使用Caffe验证了Alex Krizhevsky等人的网络构型在CIFAR-10数据集上的训练效果，其训练误差与测试误差曲线如图\ref{img:caffeError}所示

<center>![训练误差下降曲线](DeepLearningInImageRecognition/image/caffeTrainErr.png "训练误差下降曲线") ![测试误差下降曲线](DeepLearningInImageRecognition/image/caffeTestErr.png "测试误差下降曲线")<br><strong>图38 </strong>CIFAR的训练误差与测试误差</center>


由于Caffe的源代码是每100个周期对训练误差做一次测试，每500个周期对测试误差做一次测试，所以图\ref{img:caffeError}中的曲线看起来并不光滑。此外我们可以看到，训练误差有很大的波动，这是因为Alex Krizhevsky设计的网络为了避免过学习使用了dropout技巧，这个技巧会对训练集产生一个很大的惩罚，从而导致训练误差出现波动，然而这个技巧并不会对测试误差产生较大的波动。

Alex Krizhevsky设计的网络规模远远超过我们设计的网络，例如他们的网络仅特征图的数量就达几百张，而我们的网络中只有9张。从图\ref{img:caffeError}中的测试误差我们可以看到，经过5000个周期的训练后，这个网络实现了75.1\%的正确识别率，如果让网络继续训练，那么它将会收敛到文章\cite{krizhevsky2012imagenet}中号称的89\%正确率。

对于比Alex Krizhevsky设计的网络，我们的网络实现的62\%正确率看起来低得可怜，但情况似乎并没有这么糟糕，我们的网络只训练了大约300个周期后实现62\%正确率，而Alex Krizhevsky的网络训练了5000个周期实现75.1\%的正确率，如果我们横向对比，Alex Krizhevsky设计的网络在训练500个周期时得到的正确率为54.21\%，这个效果低于我们的网络效果。当然，这其中并不能排除一些因素的印象，比如我们的实验中通过对数据镜像处理将训练集规模扩大为两倍，此外，我们也没有引入避免过学习的惩罚，这种惩罚在一定程度上会降低收敛速度，但会提高最终的收敛性能。尽管如此，我们乐观地估计，如果将我们的网络规模扩大，并且延长训练周期，那么应该能实现80\%多的识别正确率。

在CIFAR-10这个任务中，我们可以看到卷积网络的威力所在，这个任务使用传统的全连接神经网络大约只能实现40\%左右的正确率，而使用模板匹配的方法基本是不可行的。卷积网络在图像识别中特征自学习的性能使得它远远超过机器学习中别的算法，目前主流的图像识别技术基本由卷积网络实现。


#结论
本文的主要目的在于介绍深度学习在图像识别中的应用，文中有两条主线贯穿全文。我们先从控制论与机器学习的关系说起，随后引入了第一个刻画数据分布的模型即受限玻尔兹曼机，为了介绍受限玻尔兹曼机的训练方法，我们讨论了马尔可夫链蒙特卡罗方法。在受限玻尔兹曼机的基础上，我们讨论了如何利用它们堆叠得到深度置信网络，并介绍了反向传播算法。至此我们完成了深度学习的第一条主线即深度置信网络的讨论。随后我们展开了第二条主线即卷积神经网络的讨论，并在其后介绍了神经网络的设计技巧与GPU高性能计算。

最后，我们通过三个实验测试了深度学习在图像识别中的识别效果。在MNIST数据集中，使用深度置信网络实现了98.7\%的识别正确率，使用卷积神经网络实现了98.9\%的识别正确率。在CIFAR-10数据集中，我们使用卷积神经网络实现了62\%的识别正确率，尽管这个结果与当前世界顶尖的结果91\%的正确率相差较远，但通过与Caffe训练的卷积网络做对比，我们乐观地认为我们的网络仍有很大的收敛空间。

深度学习作为一种特征学习，较传统模式识别方法有本质化的改变，尤其是在图像识别领域。这套方法应当值得研究人员关注。