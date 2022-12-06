"""Adding new Purchases to the Fund using a csv file"""

import pandas as pd

#FILENAME = 'Fund_Positions_Test.csv'
FILENAME = 'Fund_Positions.csv'

inventory = pd.read_csv(FILENAME, index_col=0)
purchase_data = pd.read_csv('dummy_buy_data.csv')

def reset_all_positions():
    """Sets all Position_Sizes to 0"""
    inventory.Position_Size = 0
    inventory.Position_Value = 0

def add_buy_position(item_id, quantity, price):
    """Updates purchase price, Position Size, Position Value of a newly bought item to the Fund"""
    price=price*7.4 #currently because test data in euro
    #inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] = quantity
    previous_purchase_price = inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price']
    previous_position_size = inventory.loc[inventory.Item_ID == item_id, 'Position_Size']
    inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price'] = round((previous_purchase_price*previous_position_size+price*quantity)/(previous_position_size+quantity),2)
    inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] = previous_position_size+quantity
    inventory.loc[inventory.Item_ID == item_id, 'Position_Value'] = round((previous_position_size+quantity)*inventory.loc[inventory.Item_ID==item_id, 'Value'],2)
    inventory.loc[inventory.Item_ID == item_id, 'Gain_relative'] = round(100*inventory.Position_Value[inventory.Position==name]/(inventory.Position_Size[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name])-100,2)
    inventory.loc[inventory.Item_ID == item_id, 'Gain_absolute'] = round(inventory.Position_Value[inventory.Position==name]-(inventory.Position_Size[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name]),2)

reset_all_positions()

for index, row in purchase_data.iterrows():
    add_buy_position(row['Item_Name'], row['Quantity'], row['Purchase_Price'])

# Update new percentages of the Portfolio
fonds_value = inventory['Position_Value'].sum()
inventory.Percentage = round(inventory.Position_Value/fonds_value*100,2)

#inventory.to_csv('Fonds_Position.csv')
inventory.to_csv('Fund_Positions_Test.csv')
