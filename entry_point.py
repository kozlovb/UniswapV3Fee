from common import *
from calculate_liquidity import *
from find_closest_tick import *
from calculate_fee_based_on_ticks_data import *
from brownie_request import *
from entry_point_xyz import *

# 1.
# enter current date 
# year, month, day, hour, minutes, seconds, differenceInDays = ....

# 2.
# get pool id ,  and decimals for each token :
# copy paste this into https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v3

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
# fill in the variables :
# token_0_decimals, token_1_decimals, pool_id

# 3. 
# Choose your position, fill these variables:
# amount_token1, priceA_user, priceB_user. Prices will be adjusted to closest ticks.

#4.
# If needed compare results with the one from:
# https://defi-lab.xyz/uniswapv3simulator

# Examples of 2 pools:
#  Remove """ from the example of interest

#USDC / WETH
"""

year, month, day, hour, minutes, seconds, differenceInDays = 2022, 6, 26, 23, 42, 0, 8
pool_id = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"

amount_token1 = 10
priceA_user = 0.000455544
priceB_user = 0.00124818

token_0_decimals = 6
token_1_decimals = 18
#this code results in :
#token0_fee 101.72732823020415
#token1_fee 0.08396599791129618

#defi lab results : 
#98.98
#0.08202
"""
#BTC/ETH

#"""
year, month, day, hour, minutes, seconds, differenceInDays = 2022, 6, 27, 2, 4, 0, 30
token_0_decimals = 8
token_1_decimals = 18
amount_token1 = 10
priceA_user = 15.3461
priceB_user = 20.3452
pool_id = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"

#token0_fee 0.014576350420066372
#token1_fee 0.2740428391766797
#defi lab results
#0.0149
#0.283
#"""

# This function uses information on accumulated fees stored in uniswap v3 ticks.
# Usage is explained above.
def find_fee_from_tick_data(token_0_decimals, token_1_decimals, amount_token1, priceA_user, priceB_user, 
    pool_id, year, month, day, hour, minutes, seconds, differenceInDays):

    old_block, new_block  = blocksFromDate(2022, 6, 27, 2, 4, 00, differenceInDays = 30)
    tick_l=price_to_tick(priceA_user, token_0_decimals, token_1_decimals)
    tick_u=price_to_tick(priceB_user, token_0_decimals, token_1_decimals)

    tick_low = find_closest_tick(tick_l, pool_id, old_block, max_diff=500, lower = True)
    tick_up = find_closest_tick(tick_u, pool_id, new_block, max_diff=500, lower = False)
    priceA = tick_to_price(tick_low, token_0_decimals, token_1_decimals)
    priceB =  tick_to_price(tick_up, token_0_decimals, token_1_decimals)

    results_old_block = brownie_request(old_block, pool_id, tick_low, tick_up, do_request = True)
    results_new_block = brownie_request(new_block, pool_id, tick_low, tick_up)

    L = calculate_liquidity(amount_token1, priceA, priceB, token_0_decimals, token_1_decimals, int(results_old_block["sqrt_price_x96"]))

    token0_fee, token1_fee = fee_for_tokenType(tick_low, tick_up, L, results_old_block, results_new_block)
    print("Actual price range - [", priceA, " ", priceB, " ]")
    print("token0_fee", to_regular_numbers(token0_fee, token_0_decimals, token_1_decimals, "0"))
    print("token1_fee", to_regular_numbers(token1_fee, token_0_decimals, token_1_decimals, "1"))


find_fee_from_tick_data(token_0_decimals, token_1_decimals, amount_token1, priceA_user, priceB_user, pool_id,
                        year, month, day, hour, minutes, seconds, differenceInDays)


#date UTC TODO fix to local
find_fee_from_graph_pool_data_defilab(token_0_decimals, token_1_decimals, amount_token1, priceA_user, priceB_user, pool_id,
                                  year, month, day, hour-2, minutes, seconds, differenceInDays)
