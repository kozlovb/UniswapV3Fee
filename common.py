import time
import datetime
import math 
import json
import urllib3

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
    print("my timestamp ", timestamp)

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