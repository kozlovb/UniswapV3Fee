from calculate_liquidity import *
from aggregate_fee_by_hour import *

#BTC/ETH

#old_block, new_block  = blocksFromDate(2022, 6, 27, 18, 29, 00, differenceInDays = 11)
old_block = 14974324 
new_block =15035252
token_0_decimals = 8
token_1_decimals = 18
amount_token1 = 10
priceA_user = 15.3461
priceB_user = 20.3452
pool_id = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
print("Blocks ", old_block, new_block)

tick_l = price_to_tick(priceA_user, token_0_decimals, token_1_decimals)
tick_u = price_to_tick(priceB_user, token_0_decimals, token_1_decimals)
priceA = tick_to_price(tick_l, token_0_decimals, token_1_decimals)
priceB =  tick_to_price(tick_u, token_0_decimals, token_1_decimals)


sqrt_price_x96 = get_sq_price_for_block(pool_id, old_block)


L = calculate_liquidity(amount_token1, priceA, priceB, token_0_decimals, token_1_decimals, sqrt_price_x96)

fee0, fee1 =  aggregate_fee_by_hour_when_in_range(pool_id, token_0_decimals, token_1_decimals, priceA, priceB, 2022, 6, 27, 16, 29, 00, 11)
print("fee0", fee0)
print("fee1", fee1)
print("token0_fee", to_regular_numbers(fee0, token_0_decimals, token_1_decimals, "0"))
print("token1_fee", to_regular_numbers(fee1, token_0_decimals, token_1_decimals, "1"))
