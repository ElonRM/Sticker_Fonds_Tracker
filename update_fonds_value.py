"""Updater for the value of each position and the complete Fund"""
import datetime
import pandas as pd
import requests

MAX_API_TRIES = 10
MAX_TIMEOUT = 10
# FILENAME = 'Fund_Positions_Test.csv'
FILENAME = 'Fund_Positions.csv'

def update_value_of_position(item_id, previous_price=0):
    """updates the saved value of an item using the lowest listing and
    the highest bid """
    cheapest_listing = float(get_cheapest_listing(item_id, previous_price))
    highest_bid = float(get_highest_bid(item_id, previous_price))
    if cheapest_listing/highest_bid > 1.1:
        return (round((cheapest_listing*2+highest_bid)/3,2), cheapest_listing, highest_bid)
    return (cheapest_listing, cheapest_listing, highest_bid)


def get_cheapest_listing(item_id, previous_data = 0):
    """returns the cheapest buff163 listing of an item in chinese rmb (¥)"""
    buff_api_link = f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item_id}&page_num=1&page_size=100"
    for _ in range(MAX_API_TRIES):
        api_request = requests.get(buff_api_link, timeout=MAX_TIMEOUT)
        if api_request.status_code == 200:
            data = api_request.json()
            item_listings = data["data"]["items"]
            for item_detail in item_listings:
                item_price = item_detail["price"]
                return item_price
        else:
            #print(f"Attempt {i}: buff api failed while ckecking for lowest listing for item id: {item_id}, retrying...")
            pass
    print(f"failed to check for lowest listing from buff163 api for item id: {item_id} ")
    return previous_data


def get_highest_bid(item_id, previous_data = 0):
    """return the highest buff163 bid of an item in chense rmb (¥)"""
    buff_api_link = f"https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={item_id}&page_num=1&page_size=100"
    api_request = requests.get(buff_api_link, timeout=MAX_TIMEOUT)
    for _ in range(MAX_API_TRIES):
        if api_request.status_code == 200:
            data = api_request.json()
            item_listings = data["data"]["items"]
            for item_detail in item_listings:
                item_price = item_detail["price"]
                return item_price
        else:
            #print(f"Attempt {i}: buff163 api failed to check for highest bid for item id: {item_id}, retrying...")
            pass
    print(f"failed to check for highest bid from buff163 api for item id: {item_id} ")
    return previous_data


def update_fund_value():
    """calculates the new fund value and saves it with a timestamp in the value history"""
    timestamp = datetime.datetime.now()
    absolute_value = round(inventory['Position_Value'].sum(),2)
    absolute_invested = round((inventory.Position_purchase_price*inventory.Position_Size).sum(),2)
    gain_relative = round(absolute_value/absolute_invested*100-100,2)
    gain_absolute = round(absolute_value-absolute_invested,2)
    with open(r'value_history.csv', 'a', encoding='UTF-8') as fonds_value_history:
        fonds_value_history.write(
            f"\n{timestamp},{absolute_invested},{absolute_value},{gain_relative},{gain_absolute}"
            )


if __name__ == '__main__':
    inventory = pd.read_csv(FILENAME, index_col=0)
    new_values = [update_value_of_position(item_id, price) for item_id, price in zip(inventory.Item_ID, inventory.Value)]
    values_df = pd.DataFrame(new_values, columns=['Value', 'Lowest_Listing', 'Highest_Bid'])
    print(values_df)
    inventory.Value = values_df.Value
    inventory["Lowest_Listing"] = values_df.Lowest_Listing
    inventory["Highest_Bid"] = values_df.Highest_Bid
    inventory.Position_Value = round(inventory.Value * inventory.Position_Size,2)
    inventory.Gain_relative = round(inventory.Value/inventory.Position_purchase_price*100-100, 2)
    inventory.Gain_absolute = round((inventory.Value-inventory.Position_purchase_price)*inventory.Position_Size, 2)
    fonds_value = inventory['Position_Value'].sum()
    inventory.Percentage = round(inventory.Position_Value/fonds_value*100,2)
    inventory.to_csv(FILENAME)
    update_fund_value()
