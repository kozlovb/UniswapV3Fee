# UniswapV3Fee

Two different methods have been used in order to obtain the potential fee earned on Uniswap v3.

A.
One uses data stored by uniswap for a given tick.
The function - find_fee_from_tick_data and examples are available in entry_point.py.
NOTES:
a) One has to have an infura and etherscan accounts.
It is neccesary to export env variables:
    export WEB3_INFURA_PROJECT_ID = 
    export ETHERSCAN_TOKEN
b) brownie cant get the data for every second uniswap contract. It seems that the ABI is missing as Uniswap uploads the same contract with different fee and omits part of data. Probably, it can be fixed within brownie if needed.
c) this soulution has to find an initialized tick. Thus there is a risk that exotic positions can't be simulated.
As the tick fee function will look for closest initialized ticks and they might be not found if initial position is too out of range.

B.
This solution is based on the medium article published by the defi lab.
The function name is find_fee_from_graph_pool_data_defilab.

NOTE:
 As they point out it is assumed that a position either within or out of a range during an hour. This might introduce a slight error, especially if short lasting positions are considered. This can be improved as one may track current price and when position goes out of range. Once this happens an extra call to graph data can be made.