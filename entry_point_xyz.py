from calculate_liquidity import *
from aggregate_fee_by_hour import *


#BTC/ETH
"""
year, month, day, hour, minutes, seconds, differenceInDays = 2022, 6, 27, 18, 29, 0, 11

token_0_decimals = 8
token_1_decimals = 18
amount_token1 = 10
priceA_user = 15.3461
priceB_user = 20.3452
pool_id = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
#Ressults of this function 
#token0_fee 0.0048696495789142275
#token1_fee 0.0813087261418996

# xyz result
# 0.004861
# 0.08116
"""
def find_fee_from_graph_pool_data_defilab(token_0_decimals, token_1_decimals, amount_token1, priceA_user, priceB_user, pool_id,
                                  year, month, day, hour, minutes, seconds, differenceInDays):
    old_block, new_block  = blocksFromDate(year, month, day, hour, minutes, seconds, differenceInDays)
    tick_l = price_to_tick(priceA_user, token_0_decimals, token_1_decimals)
    tick_u = price_to_tick(priceB_user, token_0_decimals, token_1_decimals)
    priceA = tick_to_price(tick_l, token_0_decimals, token_1_decimals)
    priceB =  tick_to_price(tick_u, token_0_decimals, token_1_decimals)
    

    sqrt_price_x96 = get_sq_price_for_block(pool_id, old_block)


    L = calculate_liquidity(amount_token1, priceA, priceB, token_0_decimals, token_1_decimals, sqrt_price_x96)

    fee0, fee1 = aggregate_fee_by_hour_when_in_range(pool_id, token_0_decimals, token_1_decimals, priceA, priceB, year, month, day, hour, minutes, seconds, differenceInDays, L)
    print("Actual price range - [", priceA, " ", priceB, " ]")
    print("token0_fee xyz ", to_regular_numbers(fee0, token_0_decimals, token_1_decimals, "0"))
    print("token1_fee xyz ", to_regular_numbers(fee1, token_0_decimals, token_1_decimals, "1"))


#find_fee_from_graph_pool_data_defilab(token_0_decimals, token_1_decimals, amount_token1, priceA_user, priceB_user, pool_id,
                                  #year, month, day, hour, minutes, seconds, differenceInDays)