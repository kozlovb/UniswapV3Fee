import calendar
import time
import datetime
from common import *

#Please enter UTc time !
def aggregate_fee_by_hour_when_in_range(pool_id, token_0_decimal, token_1_decimal, priceA, priceB, year, month, day, hour, minutes, seconds, differenceInDays, L):
    seconds_in_days = 86400
    s = f"{seconds}/{minutes}/{hour}/{day}/{month}/{year}"
    timestamp_now = calendar.timegm(datetime.datetime.strptime(s, "%S/%M/%H/%d/%m/%Y").timetuple())
    timestamp_old = timestamp_now - seconds_in_days * differenceInDays
    fee_prices = getFeesAndPrices(timestamp_old, timestamp_now, pool_id)
    total_fee_0 = 0
    total_fee_1 = 0
    fee_0_previous = int(fee_prices[0]["feeGrowthGlobal0X128"])
    fee_1_previous = int(fee_prices[0]["feeGrowthGlobal1X128"])
    for fee_price in fee_prices:
        price =  price_to_int(int(fee_price["sqrtPrice"]), token_0_decimal, token_1_decimal)
        if price > priceA and price < priceB:
            print("feediff", int(fee_price["feeGrowthGlobal0X128"])," ", fee_0_previous, " ",int(fee_price["feeGrowthGlobal0X128"]) - fee_0_previous)
            total_fee_0 = total_fee_0 + int(fee_price["feeGrowthGlobal0X128"]) - fee_0_previous
            total_fee_1 = total_fee_1 + int(fee_price["feeGrowthGlobal1X128"]) - fee_1_previous
        fee_0_previous = int(fee_price["feeGrowthGlobal0X128"])
        fee_1_previous = int(fee_price["feeGrowthGlobal1X128"])   
    # add up the fee here
    return L*total_fee_0, L*total_fee_1