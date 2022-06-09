import requests
import json
import pandas as pd
from find_closest_tick import *

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

#  0x000ea4a83acefdd62b1b43e9ccc281f442651520  {'symbol': 'BUSD'}   {'symbol': 'WETH'}    5508168315607950206  4794438.262787290195418958         1229.60354080782795285
# data about pool 0x4e68ccd3e89f51c3074ca5072bbac773960dfa36
# https://info.uniswap.org/#/
# -195807 may be current tick

#def tick_to_price(tick)
# examplerecent ic is -201039
# check https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf one needs to add 10^12 i.e.
#  i = log(base : 1.001, ETHprice/10^12)
#  ETHprice = 10^12 * 1.0001 ^ i


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
        feeGrowthAbove0X128 = feeGrowthGlobal0X128 - tick1_fee_Outside
    feeGrowthInside0X128 = global_fee - feeGrowthBelow0X128 - feeGrowthAbove0X128
    return feeGrowthInside0X128

def to_regular_numbers(number_128, decimal):
    return number_128/(pow(2,128)*pow(10, decimal))
#2400 mas o menos -200000
tick_up = -199980
old_block = 14914928
new_block = 14916928
tick_up_old = requests.post(url, json={'query': query(old_block, tick_up)})
tick_up_new = requests.post(url, json={'query': query(block=new_block, tick = tick_up)})
print(tick_up_old.text)
#print(tick_up_new.text)

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
liquidity  = 1
fee = calculate_fee(tick_up, tick_low, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new, liquidity)
print("RESULT", to_regular_numbers(fee, 18))


#print(json_data)

#calculate_fee(tick1, tick2, tick1_old_json[][])

#df = pd.DataFrame(json_data["data"]["pools"])
#print(df)
