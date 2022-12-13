"""adds a new item to the Funds portfolio list using the item id
 of buff163 (doesn't have to be an invested position)"""

import pandas as pd
import requests
import fund_variables as fv

fund = pd.read_csv(fv.FUND_FILENAME, index_col=0)

def add_new_position(df, item_id):
    """adds a new item to the Funds portfolio using item id"""
    buff_api_link = f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item_id}&page_num=1&page_size=100"
    if item_id in df.Item_ID.values:
        return df
    for _ in range(fv.MAX_API_TRIES):
        api_request = requests.get(buff_api_link, timeout=fv.MAX_TIMEOUT)
        if api_request.status_code == 200:
            data = api_request.json()
            item_name = data["data"]["goods_infos"][str(item_id)]["market_hash_name"]
            item_value = float(data["data"]["items"][0]["price"])
            print(item_name, item_value)
            new_position = pd.DataFrame({'Position': [item_name], 'Value': [item_value], 'Item_ID': [item_id]})
            df = pd.concat([df, new_position],ignore_index=True).fillna(0)
            return df
    print(f"failed to to find information via buff163 api using item id: {item_id} ")
    return df


ids = [773534]

for i_id in ids:
    fund = add_new_position(fund, i_id)

fund.to_csv(fv.FUND_FILENAME)
