import json
import subprocess
import time

def brownie_request(block_number, pool_address, tick_low, tick_up, do_request = True):
    print("doRequest is", do_request)
    dict_params = {
        "block_number": block_number,
        "pool_address": pool_address,
        "tick_low": tick_low,
        "tick_up": tick_up }
  
    # the json file where the params must be stored
    with open("params_brownie_request.json", "w") as out_file:
        json.dump(dict_params, out_file, indent = 4)
    if do_request:
        proc = subprocess.Popen(['sh', './run_brownie_code.sh'])
        proc.wait()

    with open('brownie_results.json') as f:
        data = json.load(f)

        return data
        """
        return (data["block_number"], data["pool_address"], data["price_x96"], data["feeGrowthGlobal0X128"], \
            data["feeGrowthGlobal1X128"], data["ticklow_fee_0_Outside"], data["ticklow_fee_1_Outside"], data["current_index"])"""

"""


tick_low = -202020
tick_up = -199980

old_block = 14767479   # (Jun-06-2022 12:13:20 PM +UTC)
new_block = 14944320   # (Jun-06-2022 08:33:23 PM +UTC)

"""



#brownie_request("14944320", "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36", -202020, -199980)