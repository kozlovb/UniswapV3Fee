

"""

1. Choose position

go to https://defi-lab.xyz/uniswapv3simulator
pick up the pool and position (for now better to take out of range but with range becoming active)
this cause defi-lab.xyz is only reliable for "active" positions.

2. Calculate liquidity

Usually x is ETH, y is USD. Price is always y/x = p.

In this case P will be like 1000-2000 usd...

from dformulas:
(x + L/sqrt(pb))(y + Lsqrt(pa)) = L^2
(y + Lsqrt(pa)) / (x + L/sqrt(pb)) = P

Ypool / Xpool = (sqrt(P) - sqrt(Pa)) / (1/sqrt(P) - 1/sqrt(Pb))
so
Ypool = Alpha * Xpool where Alpha = (sqrt(P) - sqrt(Pa)) / (1/sqrt(P) - 1/sqrt(Pb))
Say one has TotalY = 1000USD, i.e then 

Xpool * Pcurrent  + Ypool = TotalY

one can deduce;
Xpool = TotalY / (Alpha + P)
Ypool = Alpha * TotalY  / (Alpha + P)
L = Ypool / (sqrt(P) - sqrt(Pa))

In uniswap there are no doubles, so one has to convert L. Here Y is USd so 10^6, and p is sqrt(10^6/10^18) = 10^-6
thus L ->  L * 10^12.  or 
L -> L * 10^(Y_decimal - (Ydecimal - Xdecimal)/2). But we will not use this factor here, rather plug into convertion from uni numbers to real ones. 
"""
