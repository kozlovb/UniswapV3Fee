from brownie import *
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

ETH_decimals = 18
USDT_decimals = 6
pool_address = '0x4e68ccd3e89f51c3074ca5072bbac773960dfa36'
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


def getData(tick_low, tick_up, block):
    web3.eth.defaultBlock = block
    pool = Contract.from_explorer(pool_address)
    tick_values_low = pool.ticks(tick_low)
    ticklow_fee_Outside = tick_values_low['feeGrowthOutside0X128']
    tick_values_up = pool.ticks(tick_up)
    tickup_fee_Outside = tick_values_up['feeGrowthOutside0X128']
    feeGrowthGlobal0X128 = pool.feeGrowthGlobal0X128()
    ic = pool.slot0()['tick']
    return ticklow_fee_Outside, tickup_fee_Outside, ic, feeGrowthGlobal0X128

#for a given token , has tp be applied for both
def calculate_fee(tickup, ticklow, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new, liquidity):
    return liquidity * (calculate_fr(tickup, ticklow, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new) - calculate_fr(tickup, ticklow, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old))

#Taken from https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/Tick.sol
def calculate_fr(tickup, ticklow, tickup_fee_Outside, ticklow_fee_Outside, ic, global_fee):

    # calculate fee growth below
    feeGrowthBelow0X128 =0
    if ic >= ticklow:
        feeGrowthBelow0X128 = ticklow_fee_Outside
    else:
        feeGrowthBelow0X128 = global_fee - ticklow_fee_Outside
    # calculate fee growth above
    feeGrowthAbove0X128 = 0
    if ic < tickup:
        feeGrowthAbove0X128 = tickup_fee_Outside
    else:
        feeGrowthAbove0X128 = global_fee - tickup_fee_Outside
    feeGrowthInside0X128 = global_fee - feeGrowthBelow0X128 - feeGrowthAbove0X128
    return feeGrowthInside0X128

def to_regular_numbers(number_128, decimal):
    return number_128/(pow(2,128)*pow(10, decimal))
#2400 mas o menos -200000

tick_low = -202020
tick_up = -199980

old_block = 14767479   # (Jun-06-2022 12:13:20 PM +UTC)
new_block = 14944320   # (Jun-06-2022 08:33:23 PM +UTC)



#tick current is kind of strange I get -199770 which gives the price equivalent to 2111. But the price at that block was
# $2,006.51 / ETH



#--------------tick low and up old--------------------#

ticklow_fee_Outside_old, tickup_fee_Outside_old, ic_old, global_fee_old = getData(tick_low, tick_up, old_block)

#--------------tick low and up new--------------------#

ticklow_fee_Outside_new, tickup_fee_Outside_new, ic_new, global_fee_new = getData(tick_low, tick_up, new_block)



current = tick_to_price_ETH_in_USD(-202795)
print(current)
current = tick_to_price_ETH_in_USD(-199770)
print(current)
liquidity  = 250
fee = calculate_fee(tick_up, tick_low, tickup_fee_Outside_old, ticklow_fee_Outside_old, ic_old, global_fee_old, tickup_fee_Outside_new, ticklow_fee_Outside_new, ic_new, global_fee_new, liquidity)
print("RESULT in 128 numbers", fee)
print("RESULT", to_regular_numbers(fee, 18))

# 2067.346 0.00048371337
# 1685.86 0.000593169

print("price at tick up", tick_to_price_ETH_in_USD(tick_up))
print("price at tick low", tick_to_price_ETH_in_USD(tick_low))

def main():
    pass
