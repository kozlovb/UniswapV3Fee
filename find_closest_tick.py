import requests
import json
import pandas as pd
import math


url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

def query(block, tick, pool_id):
    query = '{ticks(where:{pool_contains:' +'"'+ str(pool_id) + '" '+' tickIdx_in:[' + str(tick) + ']} block:{number:' + str(block) + '}){tickIdx feeGrowthOutside0X128 feeGrowthOutside1X128 pool { tick feeGrowthGlobal0X128 feeGrowthGlobal1X128 } } }'
    return query

def tick_to_price(tick, token_0_decimals, token_1_decimals):
    return pow(1.0001,tick)*pow(10, token_0_decimals - token_1_decimals)
def price_to_tick(price, token_0_decimals, token_1_decimals):
    return math.log(price*pow(10, token_1_decimals - token_0_decimals), 1.0001)

def find_closest_tick(tick, pool_id, block, max_diff=500, lower = True):
    tick = int(tick)
    range_to_loop = range(0,0)
    if lower:
        range_to_loop = reversed(range(tick - max_diff, tick-1))
    else:
        range_to_loop = range(tick+1, tick + max_diff)

    for i in range_to_loop:
        tick_i = requests.post(url, json={'query': query(block, i, str(pool_id))})
        print("i = ", i)
        print(tick_i.text)
        json_data = json.loads(tick_i.text)
        print("json_data", json_data)
        df = pd.DataFrame(json_data["data"]["ticks"])
        if len(df) > 0:
            print("Found tick", i)
            return i


