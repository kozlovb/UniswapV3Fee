import requests
import json
import pandas as pd
from find_closest_tick import *
import math
"""
Jun 11, 14.50.       - 30 days.     13 May 14.50
# check data
Block now 14944320
Block 30 days ago
14767479

WETH
0.03111
USDT
57.18

You can get the block number by timestamp, using etherscan's API:
https://www.epochconverter.com
https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=1652446239&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN

pool id
"""




url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

ETH_decimals  = 18
USDT_decimals  = 6
# data about pool 0x4e68ccd3e89f51c3074ca5072bbac773960dfa36
# https://info.uniswap.org/#/

#data about token like name decimals ..
# https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3/graphql?query=query+MyQuery+%7B%0A++pool%28id%3A+%220x4e68ccd3e89f51c3074ca5072bbac773960dfa36%22%29+%7B%0A++++token0+%7B%0A++++++symbol%0A++++++decimals%0A++++%7D%0A++%7D%0A%7D

def tick_to_price(tick, decimals):
    return pow(1.0001,tick) / pow(10, decimals)
def tick_to_price_ETH_in_USD(tick):
    return pow(1.0001,tick)*pow(10, ETH_decimals-USDT_decimals)
def price_to_tick(price, decimals):
    math.log(price, 1.001)/pow(10, decimals)
# example present tick ic is -201039
# check https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf one needs to add 10^12 i.e.



# -196256 3k
# -203188 1.5K

#for a given token , has tp be applied for both
def calculate_fee(tickup, ticklow, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new, liquidity):
    return liquidity * (calculate_fr(tickup, ticklow, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new) - calculate_fr(tickup, ticklow, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old))

def calculate_fr(tickup, ticklow, tick1_fee_Outside, tick2_fee_Outside, ic, global_fee):
    #Zaherachit to ge samoe no v pythone
    # calculate fee growth below
    feeGrowthBelow0X128 =0
    if ic >= ticklow:
        feeGrowthBelow0X128 = tick2_fee_Outside
    else:
        feeGrowthBelow0X128 = global_fee - tick2_fee_Outside;
    # calculate fee growth above
    feeGrowthAbove0X128 = 0
    if ic < tickup:
        feeGrowthAbove0X128 = tick1_fee_Outside
    else:
        feeGrowthAbove0X128 = global_fee - tick1_fee_Outside
    feeGrowthInside0X128 = global_fee - feeGrowthBelow0X128 - feeGrowthAbove0X128
    return feeGrowthInside0X128

def to_regular_numbers(number_128, decimal):
    return number_128/(pow(2,128)*pow(10, decimal))
#2400 mas o menos -200000


tick_up = -199980

old_block = 14767479   # (Jun-06-2022 12:13:20 PM +UTC)
new_block = 14944320   # (Jun-06-2022 08:33:23 PM +UTC)
tick_up_old = requests.post(url, json={'query': query(old_block, tick_up)})
tick_up_new = requests.post(url, json={'query': query(block=new_block, tick = tick_up)})

json_data = json.loads(tick_up_old.text)
tickup_fee_Outside_old = int(json_data["data"]["ticks"][0]["feeGrowthOutside0X128"])
ic_old = int(json_data["data"]["ticks"][0]["pool"]["tick"])
global_fee_old = int(json_data["data"]["ticks"][0]["pool"]["feeGrowthGlobal0X128"])

json_data = json.loads(tick_up_new.text)
tickup_fee_Outside_new = int(json_data["data"]["ticks"][0]["feeGrowthOutside0X128"])
ic_new  = int(json_data["data"]["ticks"][0]["pool"]["tick"])
global_fee_new = int(json_data["data"]["ticks"][0]["pool"]["feeGrowthGlobal0X128"])
#1700
tick_low = -202020
tick_low_old = requests.post(url, json={'query': query(block=old_block, tick = tick_low)})
tick_low_new = requests.post(url, json={'query': query(block=new_block, tick = tick_low)})

json_data = json.loads(tick_low_old.text)
ticklow_fee_Outside_old = int(json_data["data"]["ticks"][0]["feeGrowthOutside0X128"])
json_data = json.loads(tick_low_new.text)
ticklow_fee_Outside_new = int(json_data["data"]["ticks"][0]["feeGrowthOutside0X128"])
#print("Found this results", tickup_fee_Outside_old, ic_old, global_fee_old)
liquidity  = 250
fee = calculate_fee(tick_up, tick_low, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new, liquidity)
print("RESULT", to_regular_numbers(fee, 18))

# 2067.346 0.00048371337
# 1685.86 0.000593169

print("price at tick up", tick_to_price_ETH_in_USD(tick_up))
print("price at tick low", tick_to_price_ETH_in_USD(tick_low))
