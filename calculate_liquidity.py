import math 
from common import *

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
or
L = Xtool / (1/sqrt(P) - 1/sqrt(Pb))

In uniswap there are no doubles, so one has to convert L. Here Y is USd so 10^6, and p is sqrt(10^6/10^18) = 10^-6
thus L ->  L * 10^12.  or 
L -> L * 10^(Y_decimal - (Ydecimal - Xdecimal)/2). But we will not use this factor here, rather plug into convertion from uni numbers to real ones. 

usdt pool 0x4e68ccd3e89f51c3074ca5072bbac773960dfa36

"""


# Amount is the toke "1", so the second token
def calculate_liquidity(amount, priceA, priceB, token_0_decimals, token_1_decimals, results_old_block):
    Xpool = 0
    Ypool = 0
    L = 0
    price = price_to_int(int(results_old_block["sqrt_price_x96"]), token_0_decimals, token_1_decimals)
    if price > priceB:
        Ypool = amount
        L = Ypool / (math.sqrt(price) - math.sqrt(priceA))
    elif price < priceA:
        Xpool = amount / price
        L = Xpool * (1/math.sqrt(price) - 1/math.sqrt(priceB))
    else:
        Alpha = (math.sqrt(price) -  math.sqrt(priceA)) / ( (1 / math.sqrt(price)) - (1 / math.sqrt(priceB)) )   
        Xpool = amount / (Alpha + price)
        Ypool = Alpha * amount  / (Alpha + price)                           
        L = Ypool / (math.sqrt(price) - math.sqrt(priceA))
    return L

def main():
    pass


