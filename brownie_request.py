import json
import subprocess

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