#from brownie import *
from common import *

"""Before running the script

export WEB3_INFURA_PROJECT_ID=a3efd95ef45e49a3aa7876780d804743
export ETHERSCAN_TOKEN=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN

to run script - 
brownie run request_fee_brownie_both_tokens.py --network mainnet

"""


"""
Jun 11, 14.50.       - 30 days.     13 May 14.50
# check data
Block now 14944320
Block 30 days ago
14767479

14767479
14761163 14944320

WETH
0.03111
USDT
57.18

I get in 128 numbers
eth fee 11574384108554583759687502894128478529368500
(fee/2^128)/10^6 = 0.034
usd fee 20675291796253282454046314285851000
(fee/s^128)*10^6 = 60,75

You can get the block number by timestamp, using etherscan's API:
https://www.epochconverter.com
https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=1652446239&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN

pool id
"""




#url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'





#for a given token , has to be applied for both
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



def fee_for_tokenType(tick_low, tick_up, L, results_old_block, results_new_block):
    token_0_fee = calculate_fee(tick_up, tick_low, results_old_block["tickup_fee_0_Outside"], results_old_block["ticklow_fee_0_Outside"], 
     results_old_block["current_index"], results_old_block["feeGrowthGlobal0X128"], results_new_block["tickup_fee_0_Outside"], 
     results_new_block["ticklow_fee_0_Outside"], results_new_block["current_index"], results_new_block["feeGrowthGlobal0X128"], L)
    token_1_fee = calculate_fee(tick_up, tick_low, results_old_block["tickup_fee_1_Outside"], results_old_block["ticklow_fee_1_Outside"], 
     results_old_block["current_index"], results_old_block["feeGrowthGlobal1X128"], results_new_block["tickup_fee_1_Outside"], 
     results_new_block["ticklow_fee_1_Outside"], results_new_block["current_index"], results_new_block["feeGrowthGlobal1X128"], L) 
    return token_0_fee, token_1_fee

def main():
    pass
