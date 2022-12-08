"""Updater for the value of each position and the complete Fund"""
import datetime
import pandas as pd
import requests
import fund_variables as fv

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
    for _ in range(fv.MAX_API_TRIES):
        api_request = requests.get(buff_api_link, timeout=fv.MAX_TIMEOUT)
        if api_request.status_code == 200:
            data = api_request.json()
            item_listings = data["data"]["items"]
            for item_detail in item_listings:
                item_price = item_detail["price"]
                return item_price
        else:
            # print(f"Attempt {i}: buff api failed while ckecking for lowest listing for item id: {item_id}, retrying...")
            pass
    print(f"failed to check for lowest listing from buff163 api for item id: {item_id}")
    return previous_data


def get_highest_bid(item_id, previous_data = 0):
    """return the highest buff163 bid of an item in chense rmb (¥)"""

    buff_api_link = f"https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={item_id}&page_num=1&page_size=100"
    api_request = requests.get(buff_api_link, timeout=fv.MAX_TIMEOUT)
    for _ in range(fv.MAX_API_TRIES):
        if api_request.status_code == 200:
            data = api_request.json()
            item_listings = data["data"]["items"]
            for item_detail in item_listings:
                item_price = item_detail["price"]
                return item_price
        else:
            #print(f"Attempt {i}: buff163 api failed to check for highest bid for item id: {item_id}, retrying...")
            pass
    print(f"failed to check for highest bid from buff163 api for item id: {item_id}")
    return previous_data


def save_fund_value(fund, liquid_funds):
    """calculates the new fund value, relative and absolute gain and
    saves it with a timestamp in the fund value history"""

    timestamp = datetime.datetime.now()
    absolute_invested = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0).iloc[0]['Amount_Invested']

    absolute_value = round(fund['Position_Value'].sum()+liquid_funds,2)
    gain_relative = round(absolute_value/absolute_invested*100-100,2)
    gain_absolute = round(absolute_value-absolute_invested,2)

    fund_value_history = pd.read_csv(fv.FUND_VALUE_HISTORY,index_col=0)
    fund_value_history= pd.concat([fund_value_history, pd.DataFrame({'Timestamp': timestamp,
                                'Total_invested': [absolute_invested],
                                'Total_value': [absolute_value],
                                'Return_relative': [gain_relative],
                                'Return_absolute': [gain_absolute]})]
                                )
    fund_value_history.to_csv(fv.FUND_VALUE_HISTORY)


def update_fund_value(fund, liquid_funds):
    """updates the funds value and saves it into fund_value_history.csv"""

    new_values = [update_value_of_position(item_id, price) for item_id, price in zip(fund.Item_ID, fund.Value)]
    values_df = pd.DataFrame(new_values, columns=['Value', 'Lowest_Listing', 'Highest_Bid'])
    fund.Value = values_df.Value

    fund.Lowest_Listing = values_df.Lowest_Listing
    fund.Highest_Bid = values_df.Highest_Bid
    fund.Position_Value = round(fund.Value * fund.Position_Size,2)
    fund.Gain_relative = round(fund.Value/fund.Position_purchase_price*100-100, 2)
    fund.Gain_absolute = round((fund.Value-fund.Position_purchase_price)*fund.Position_Size, 2)


    #liquid_funds = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0).iloc[0]['Liquid_Funds']
    fund_value = round(fund['Position_Value'].sum()+liquid_funds,2)
    fund.Percentage = round(fund.Position_Value/fund_value*100,2)
    return fund


if __name__ == '__main__':
    fnd = pd.read_csv(fv.FUND_FILENAME, index_col=0)
    lqd_funds = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0).iloc[0]['Liquid_Funds']
    fnd = update_fund_value(fnd, lqd_funds)

    save_fund_value(fnd, lqd_funds)

    fnd.to_csv(fv.FUND_FILENAME)
