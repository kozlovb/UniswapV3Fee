from brownie import *
import json

def getData():
    with open('params_brownie_request.json') as f:
        data = json.load(f)
        web3.eth.defaultBlock = int(data["block_number"])
        pool = Contract.from_explorer(data["pool_address"])
        tick_low = int(data["tick_low"])
        tick_up = int(data["tick_up"])
        sqrt_price_x96 = pool.slot0()['sqrtPriceX96']
        tick_values_low = pool.ticks(tick_low)
        tick_values_up = pool.ticks(tick_up)
        dict_results = {
        "block_number": data["block_number"],
        "pool_address": data["pool_address"],
        "sqrt_price_x96": sqrt_price_x96,
        "feeGrowthGlobal0X128" : pool.feeGrowthGlobal0X128(),
        "feeGrowthGlobal1X128" : pool.feeGrowthGlobal1X128(),
        "ticklow_fee_0_Outside" : tick_values_low['feeGrowthOutside0X128'],
        "ticklow_fee_1_Outside" : tick_values_low['feeGrowthOutside1X128'],
        "tickup_fee_0_Outside" : tick_values_up['feeGrowthOutside0X128'],
        "tickup_fee_1_Outside" : tick_values_up['feeGrowthOutside1X128'],
        "current_index" : pool.slot0()['tick']
        }
        with open("brownie_results.json", "w") as out_file:
            json.dump(dict_results, out_file, indent = 4)

        
getData()
def main():
    pass