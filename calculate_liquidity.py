#from brownie import *
import time
import datetime
import math 
import json
import urllib3
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
"""

ETH_decimals = 18
USDT_decimals = 6

pool_address = '0x4e68ccd3e89f51c3074ca5072bbac773960dfa36'

# parameters date, amount in USD, priceA , priceB
# return tick_low, tick_up, L (without decimal factor)
# Xpool, Y pool printed but for now doesn't metter, will metter for impermanent loss though.
def get_price_for_block(block_number, pool_address):
    web3.eth.defaultBlock = block_number
    pool = Contract.from_explorer(pool_address)
    sqrt_price_x96 = pool.slot0()['sqrtPriceX96']
    print("sqrt_price_x96", sqrt_price_x96)
    sqrt_price = sqrt_price_x96 / (pow(2,96) * pow(10, (USDT_decimals - ETH_decimals) / 2 ))
    print("Price for block",  sqrt_price * sqrt_price)
    return sqrt_price * sqrt_price

def price_to_int(sqrt_price_x96, token_0_decimal, token_1_decimal):
    print("sqrt_price_x96", sqrt_price_x96)
    sqrt_price = sqrt_price_x96 / (pow(2,96) * pow(10, (token_1_decimal - token_0_decimal) / 2 ))
    print("Price for block",  sqrt_price * sqrt_price)
    return sqrt_price * sqrt_price

### NORE: all in current timezone
def blocksFromDate(year, month, day, hour, minutes, seconds, differenceInDays):
    # get linux timestamp
    seconds_in_days = 86400
    block_now = 0
    block_early = 0
    s = f"{seconds}/{minutes}/{hour}/{day}/{month}/{year}"
    timestamp  = time.mktime(datetime.datetime.strptime(s, "%S/%M/%H/%d/%m/%Y").timetuple())
    http = urllib3.PoolManager()
    print("my timestamp ", timestamp)

    url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=' + str(int(timestamp)) + '&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN'
    resp = http.request('GET', url)
    result  = json.loads(resp.data)
    block_now = int(result['result'])

    url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=' + str(int(timestamp)-differenceInDays*seconds_in_days) + '&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN'
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    result  = json.loads(resp.data)
    block_early = int(result['result'])
    return block_early, block_now

def calculate_liquidity_A(amount, priceA, priceB, token_0_decimals, token_1_decimals, results_old_block):
    Xpool = 0   # ETH
    Ypool = 0   # USD
    L = 0
    price = price_to_int(int(results_old_block["sqrt_price_x96"]), token_0_decimals, token_1_decimals)
    print("Price is ", price)
    #Price = 2006
    #Which price to take ??? 
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
    
def calculate_liquidity(block_number, amountUSD, priceA, priceB):
    Xpool = 0   # ETH
    Ypool = 0   # USD
    L = 0
    # 1 find ticks, cause we need to adjust Pa and Pb to actual possible ones 
    # ticks has to exist .... that's another problem with this solution if tick is dead then ... there are no data.
    # may be there is a way top fix that by taking feeAccumulated from neighbouting tick and then switching to actual once but may be not.
    Price = get_price_for_block(block_number, pool_address)
    #Price = 2006
    #Which price to take ??? 
    if Price > priceB:
        print("in Price > priceB")
        Ypool = amountUSD
        L = Ypool / (math.sqrt(Price) - math.sqrt(priceA))
    elif Price < priceA:
        print("in Price < priceA")
        Xpool = amountUSD / Price
        L = Xpool * (1/math.sqrt(Price) - 1/math.sqrt(priceB))
    else:
        Alpha = (math.sqrt(Price) -  math.sqrt(priceA)) / ( (1 / math.sqrt(Price)) - (1 / math.sqrt(priceB)) )   
        Xpool = amountUSD / (Alpha + Price)
        Ypool = Alpha * amountUSD  / (Alpha + Price)                           
        L = Ypool / (math.sqrt(Price) - math.sqrt(priceA))
    return L

#L_test = calculate_liquidity(14767479, 1000, 1685, 2067)
#print("L_test is ", L_test)



# If liquidity is taken with Price = 2006 , price from the block then L = 226.990 - results will be very close to defi lab ones
# If I take Price from uniswap at that moment then L = 204. then return is 10% lower... 

def main():
    pass


