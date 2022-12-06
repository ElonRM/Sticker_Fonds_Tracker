"""Adding new Purchases to the Fund using a csv file"""

import pandas as pd

#FILENAME = 'Fund_Positions_Test.csv'
FILENAME = 'Fund_Positions.csv'
LIQUID_FUNDS = 'Liquid_Funds.csv'

inventory = pd.read_csv(FILENAME, index_col=0)
purchase_data = pd.read_csv('new_purchases.csv')

def reset_all_positions():
    """Sets all Position_Sizes to 0"""
    inventory.Position_Size = 0
    inventory.Position_Value = 0

def add_buy_position(item_id, quantity, price):
    """Updates purchase price, Position Size, Position Value of a newly bought item to the Fund"""
    previous_purchase_price = inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price']
    previous_position_size = inventory.loc[inventory.Item_ID == item_id, 'Position_Size']
    item_value = inventory.loc[inventory.Item_ID==item_id, 'Value']

    new_position_size = previous_position_size+quantity
    new_purchase_price = round((previous_purchase_price*previous_position_size+price*quantity)/(new_position_size),2)
    new_position_value = round(new_position_size*item_value,2)
    new_gain_relative = round(100*item_value/new_purchase_price-100,2)
    new_gain_absolute = round(new_position_size*(item_value-new_purchase_price),2)

    inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price'] = new_purchase_price
    inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] = new_position_size
    inventory.loc[inventory.Item_ID == item_id, 'Position_Value'] = new_position_value
    inventory.loc[inventory.Item_ID == item_id, 'Gain_relative'] = new_gain_relative
    inventory.loc[inventory.Item_ID == item_id, 'Gain_absolute'] = new_gain_absolute

#reset_all_positions()

for index, row in purchase_data.iterrows():
    add_buy_position(row['Item_ID'], row['Quantity'], row['Purchase_Price'])
    #pass

# Update new percentages of the Portfolio
liquid_funds = pd.read_csv(LIQUID_FUNDS, index_col=0).iloc[0]['Liquid_Funds']
fund_value = inventory['Position_Value'].sum()
print(fund_value, liquid_funds)
inventory.Percentage = round(inventory.Position_Value/(fund_value+liquid_funds)*100,2)

inventory.to_csv(FILENAME)
