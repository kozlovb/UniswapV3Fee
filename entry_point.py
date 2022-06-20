import json
from calculate_liquidity import *
from find_closest_tick import *
from request_fee_brownie_both_tokens import *
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
  }
  token1 {
    symbol 
  }
  feeTier
 }
}
"""

#USDC / WETH
pool_id  = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
amount_UCDC = 1000
priceA = 1199.97
priceB = 2499.91
# date1 = 00/26/13/20/06/2022


old_block, new_block  = blocksFromDate(0, 26, 13, 20, 6, 2022, differenceInDays = 30)

tick_low = find_closest_tick(tick, block_eary = 14914928, max_diff=500, lower = True)
tick_up = find_closest_tick(tick, block_now = 14914928, max_diff=500, lower = False)

L = calculate_liquidity(old_block, amount_UCDC, priceA, priceB)
token0_fee = fee_for_tokenType_brownie(tick_low, tick_up, new_block, old_block, L, "0")
token1_fee = fee_for_tokenType_brownie(tick_low, tick_up, new_block, old_block, L, "1")

def main():
    pass



