import json
from common import *
from calculate_liquidity import *
from find_closest_tick import *
from calculate_fee_based_on_ticks_data import *
from brownie_request import *
# Enter 2 timestamps -> getting blocks 
# Enter amount in USD
# Calculate fee
# Calculate impermanent loss ? 

# https://defi-lab.xyz/uniswapv3simulator

#get pool id , copy paste this into https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v3

"""
{
 pools(first: 1000, orderBy: volumeUSD, orderDirection: desc) {
   id
  token0 {
    symbol
    decimals
  }
  token1 {
    symbol 
    decimals
  }
  feeTier
 }
}
"""


"""

old_block, new_block  = blocksFromDate(2022, 6, 26, 0, 18, 50, differenceInDays = 30)

token_0_decimals = 18
token_1_decimals = 6
pool_id = '0x4e68ccd3e89f51c3074ca5072bbac773960dfa36'
amount_token1 = 1000
priceA_user = 1006.32
priceB_user = 1636
"""
#result token0_fee 0.036181617173859856
# result token1_fee 41.372097991389566
# result defy lab 0.04276
#result defy lab 49.16








#USDC / WETH
"""
old_block, new_block  = blocksFromDate(2022, 6, 26, 23, 42, 00, differenceInDays = 8)

pool_id = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"

amount_token1 = 10
priceA_user = 0.000455544
priceB_user = 0.00124818

token_0_decimals = 6
token_1_decimals = 18
this code results:
token0_fee 101.72732823020415
token1_fee 0.08396599791129618

defi lab results : 
98.98
0.08202
"""
#BTC/ETH

old_block, new_block  = blocksFromDate(2022, 6, 27, 2, 4, 00, differenceInDays = 30)
token_0_decimals = 8
token_1_decimals = 18
amount_token1 = 10
priceA_user = 15.3461
priceB_user = 20.3452
pool_id = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
print("Blocks ", old_block, new_block)
#token0_fee 0.014576350420066372
#token1_fee 0.2740428391766797
#defi lab results
#0.0149
#0.283

tick_l=price_to_tick(priceA_user, token_0_decimals, token_1_decimals)
tick_u=price_to_tick(priceB_user, token_0_decimals, token_1_decimals)
print("tick_l", tick_l, "tick_u", tick_u)

tick_low = find_closest_tick(tick_l, pool_id, old_block, max_diff=500, lower = True)
tick_up = find_closest_tick(tick_u, pool_id, new_block, max_diff=500, lower = False)
priceA = tick_to_price(tick_low, token_0_decimals, token_1_decimals)
priceB =  tick_to_price(tick_up, token_0_decimals, token_1_decimals)
print("found tick_low", tick_low, "found tick_up", tick_up)
print("Actual priceA (low) ", priceA , "initial users price", priceA_user)
print("Actual priceB (low) ", priceB , "initial users price", priceB_user)

results_old_block = brownie_request(old_block, pool_id, tick_low, tick_up, do_request = True)
results_new_block = brownie_request(new_block, pool_id, tick_low, tick_up)

L = calculate_liquidity(amount_token1, priceA, priceB, token_0_decimals, token_1_decimals, results_old_block)
print("Liquidity ", L)
token0_fee, token1_fee = fee_for_tokenType(tick_low, tick_up, L, results_old_block, results_new_block)

print("token0_fee", to_regular_numbers(token0_fee, token_0_decimals, token_1_decimals, "0"))
print("token1_fee", to_regular_numbers(token1_fee, token_0_decimals, token_1_decimals, "1"))

def main():
    pass



