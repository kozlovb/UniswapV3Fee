import requests
from brownie import *


#this file is taken from someones github
#it proves that unfortunately the graph has just the wrong data ....

pool_address = "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36"
tick = "-199980"
block_number = 14767479
query = """
query {
  ticks(where:{pool_contains:"%s",tickIdx:%s}
        block:{number:%s})
  {
      tickIdx
      feeGrowthOutside0X128
      feeGrowthOutside1X128
   }
}
""" % (pool_address, tick, block_number)


def run_query(q):
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
                            '',
                            json={'query': query})
    return request.json()


web3.eth.defaultBlock = block_number
pool = Contract.from_explorer(pool_address)
tick_values = pool.ticks(tick)
feeGrowthGlobal0X128 =   pool.feeGrowthGlobal0X128()
print("blockchaion feeGrowthGlobal0X128", feeGrowthGlobal0X128)

print("pool.slot0.tick", pool.slot0())


graph_resp = run_query(query)

print("-----------------------------")
print(f"Testing contract calls vs the graph values for\npool:%s\ntick:%s\nblock:%s" %
      (pool_address, tick, block_number))

print(f"feeGrowthOutside0X128 from the blockchain: %s" %
      tick_values['feeGrowthOutside0X128'])

print(f"feeGrowthOutside0X128 from the graph     : %s" %
      graph_resp['data']['ticks'][0]['feeGrowthOutside0X128'])

if graph_resp['data']['ticks'][0]['feeGrowthOutside0X128'] == tick_values['feeGrowthOutside0X128']:
    print("Match ✓")
else:
    print("Mismatch ✘")

def main():
    pass
