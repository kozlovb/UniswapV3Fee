import time
import datetime
import math 
import json
import urllib3
import requests

def price_to_int(sqrt_price_x96, token_0_decimal, token_1_decimal):
    sqrt_price = sqrt_price_x96 / (pow(2,96) * pow(10, (token_1_decimal - token_0_decimal) / 2 ))
    return sqrt_price * sqrt_price

### NORE: all in current timezone
def blocksFromDate(year, month, day, hour, minutes, seconds, differenceInDays):
    seconds_in_days = 86400
    block_now = 0
    block_early = 0
    s = f"{seconds}/{minutes}/{hour}/{day}/{month}/{year}"
    timestamp  = time.mktime(datetime.datetime.strptime(s, "%S/%M/%H/%d/%m/%Y").timetuple())
    http = urllib3.PoolManager()

    url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=' + str(int(timestamp)) + '&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN'
    resp = http.request('GET', url)
    result  = json.loads(resp.data)
    block_now = int(result['result'])

    url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=' + str(int(timestamp)-differenceInDays*seconds_in_days) + '&closest=before&apikey=ABRCM9H8AIM911I5H7GNGDU9EJU53YCGCN'
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    result  = json.loads(resp.data)
    block_early = int(result['result'])
    return block_early, block_now

def to_regular_numbers(number_128, t0_decimals, t1_decimals, tokenIndex):
    liquidity_coef = t0_decimals - ((t0_decimals - t1_decimals)/2)
    decimal_coef = 0
    if tokenIndex == '0':
        decimal_coef = liquidity_coef - t0_decimals
    else:
        decimal_coef = liquidity_coef - t1_decimals
    return (number_128/(pow(2,128))) * pow(10, decimal_coef)

def tick_to_price(tick, token_0_decimals, token_1_decimals):
    return pow(1.0001,tick)*pow(10, token_0_decimals - token_1_decimals)

def price_to_tick(price, token_0_decimals, token_1_decimals):
    return math.log(price*pow(10, token_1_decimals - token_0_decimals), 1.0001)

def get_sq_price_for_block(pool_id, old_block):
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    query = '{ pool( id: "'+str(pool_id)+'" block: {number: '+str(old_block)+'}) {sqrtPrice} }'
    result = requests.post(url, json={'query': query})
    json_data = json.loads(result.text)
    return int(json_data["data"]["pool"]["sqrtPrice"])

def getFeesAndPrices(timestamp_old, timestamp_now, pool_id):
    number_of_hours = (int(timestamp_now) - int(timestamp_old))/3600 + 1
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    query ="""{
    poolHourDatas(
        where: {pool_contains: "%s", periodStartUnix_gte: %s}
        first : %s
        orderBy : periodStartUnix
        orderDirection : asc
      ) {
        periodStartUnix
        feeGrowthGlobal0X128
        feeGrowthGlobal1X128
        sqrtPrice
      }
    }""" % (str(pool_id), str(timestamp_old), str(int(number_of_hours)))
    
    result = requests.post(url, json={'query': query})
    json_data = json.loads(result.text)
    
    return json_data["data"]["poolHourDatas"]



    """{
  poolHourDatas(
    where: {pool_contains: "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed", periodStartUnix_gte: 1655731210}
    first : 200
    orderBy : periodStartUnix
    orderDirection : asc
  ) {
    periodStartUnix
    feeGrowthGlobal0X128
    feeGrowthGlobal1X128
    sqrtPrice
  }
}"""