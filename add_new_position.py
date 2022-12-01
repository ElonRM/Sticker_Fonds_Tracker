"""adds a new item to the Funds portfolio list using the item id
 of buff163 (doesn't have to be an invested position)"""

import pandas as pd
import requests

FILENAME = "Fund_Positions_Test.csv"
FILENAME2 = "Fund_Positions_Test.csv"
MAX_API_TRIES = 20
MAX_TIMEOUT = 15

df = pd.read_csv(FILENAME, index_col=0)

def add_new_position(item_id):
    """adds a new item to the Funds portfolio using item id"""
    buff_api_link = f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item_id}&page_num=1&page_size=100"
    print(item_id in df.Item_ID.values)
    if item_id in df.Item_ID.values:
        return
    for _ in range(MAX_API_TRIES):
        api_request = requests.get(buff_api_link, timeout=MAX_TIMEOUT)
        if api_request.status_code == 200:
            data = api_request.json()
            item_name = data["data"]["goods_infos"][str(item_id)]["market_hash_name"]
            item_value = data["data"]["items"][0]["price"]
            print(item_name, item_value)
            break
    #print(f"failed to to find information via buff163 api using item id: {item_id} ")
    new_position = {'Position': item_name, 'Position_Size': 0, 'Item_ID': item_id}
    df2 = df.append(new_position, ignore_index = True).fillna(0)
    df2.to_csv(FILENAME2)

add_new_position(894465)
