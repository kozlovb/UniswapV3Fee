import requests
import json
import pandas as pd


query = """{
  pools(first: 5) {
    id
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    liquidity
    volumeToken0
    volumeToken1
  }
}
"""

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)


json_data = json.loads(r.text)
print(json_data)

df = pd.DataFrame(json_data["data"]["pools"])
print(df)
