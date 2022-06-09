import requests
import json
import pandas as pd

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

query = """
{
  pool({id:"0x4e68ccd3e89f51c3074ca5072bbac773960dfa36"})
  {
    liquidity
    token0 {symbol decimals}
  }
}"""

pool = requests.post(url, json={'query': query})
print(pool.text)
