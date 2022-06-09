import requests
import json
import pandas as pd

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

def query(block, tick):
    query = '{ticks(where:{pool_contains:"0x4e68ccd3e89f51c3074ca5072bbac773960dfa36" tickIdx_in:[' + str(tick) + ']} block:{number:' + str(block) + '}){tickIdx feeGrowthOutside0X128 feeGrowthOutside1X128 pool { tick feeGrowthGlobal0X128 feeGrowthGlobal1X128 } } }'
    #print ("we get query")
    #print(query)
    return query

def find_closest_tick(tick, block = 14914928, max_diff=500, lower = True):
    range_to_loop = range(0,0)
    if lower:
        range_to_loop = reversed(range(tick - max_diff, tick-1))
    else:
        range_to_loop = range(tick+1, tick + max_diff)

    for i in range_to_loop:
        tick_i = requests.post(url, json={'query': query(block, i)})
        print("i = ", i)
        print(tick_i.text)
        json_data = json.loads(tick_i.text)
        df = pd.DataFrame(json_data["data"]["ticks"])
        if len(df) > 0:
            print("Found tick", i)
            return i

#find_closest_tick(-202000, block = 14914928, max_diff=500, lower = True)
