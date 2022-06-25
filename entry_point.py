import json
from calculate_liquidity import *
from find_closest_tick import *
from request_fee_brownie_both_tokens import *
from fee_for_tokenType_brownie import *
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

#1 test WETH/USDT pool
tick_low = -202020
tick_up = -199980

#old_block = 14767479   # (Jun-11-2022 14/50 PM +UTC)
#new_block = 14944320   # (Jun-11-2022 12:47:33 PM +UTC)  $ 00/50/14/01/06/2022
#def blocksFromDate(year, month, day, hour, minutes, seconds, differenceInDays):
token_0_decimals = 18
token_1_decimals = 6
pool_id = '0x4e68ccd3e89f51c3074ca5072bbac773960dfa36'
amount_token1 = 1000
priceA_user = 1685
priceB_user = 2067

#old_block = 14767479
"""
#USDC / WETH
pool_id  = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
amount_token0 = 1
priceA = 1199.97
priceB = 2499.91
# date1 = 00/26/13/20/06/2022
token_0_decimals = 6
token_1_decimals = 18
"""

old_block, new_block  = blocksFromDate(2022, 6, 11, 14, 47, 33, differenceInDays = 30)
print("Blocks ", old_block, new_block)

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

results_old_block = brownie_request(old_block, pool_address, tick_low, tick_up, do_request = True)
results_new_block = brownie_request(new_block, pool_address, tick_low, tick_up)

L = calculate_liquidity_A(amount_token1, priceA, priceB, token_0_decimals, token_1_decimals, results_old_block)
print("Liquidity ", L)
token0_fee, token1_fee = fee_for_tokenType_A(tick_low, tick_up, L, results_old_block, results_new_block)

print("token0_fee", to_regular_numbers(token0_fee, token_0_decimals, token_1_decimals, "0"))
print("token1_fee", to_regular_numbers(token1_fee, token_0_decimals, token_1_decimals, "1"))

def main():
    pass



