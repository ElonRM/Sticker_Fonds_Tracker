""" Adds Functionality to sell a specific amout of a position,
 calculates the selling fees and adds the gained money to liquid funds"""

import pandas as pd

FILENAME = 'Fund_Positions.csv'
LIQUID_FUNDS = 'Liquid_Funds.csv'
SELL_DATA = pd.read_csv('new_sells.csv')

def sell_position(item_id, quantity, price):
    """ sells the item Using item_id and updates available liquid funds """
    gained_funds = round(int(price*100*0.975)/100*quantity,2)
    funds.Liquid_Funds += gained_funds

    new_position_size = inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] - quantity
    item_value = inventory.loc[inventory.Item_ID == item_id, 'Value']

    inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] = new_position_size
    inventory.loc[inventory.Item_ID == item_id, 'Position_Value'] = new_position_size*item_value
    inventory.loc[inventory.Item_ID == item_id, 'Gain_absolute'] = new_position_size*(item_value-inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price'])

    fund_value = inventory['Position_Value'].sum()+funds.iloc[0]['Liquid_Funds']
    inventory.Percentage = round(inventory.Position_Value/fund_value*100,2)

    funds.to_csv(LIQUID_FUNDS)
    inventory.to_csv(FILENAME)


if __name__ == '__main__':
    inventory = pd.read_csv(FILENAME, index_col=0)
    funds = pd.read_csv(LIQUID_FUNDS, index_col=0)
    for index, row in SELL_DATA.iterrows():
        sell_position(row['Item_ID'], row['Quantity'], row['Sell_Price'])