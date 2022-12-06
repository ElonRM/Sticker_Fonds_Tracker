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

def add_buy_position(name, position_size, price):
    """Updates purchase price, Position Size, Position Value of a newly bought item to the Fund"""
    price=price*7.4 #currently because test data in euro
    inventory.Position_purchase_price[inventory.Position == name] = round((inventory.Position_purchase_price[inventory.Position==name]*inventory.Position_Size[inventory.Position==name]+price*position_size)/(inventory.Position_Size[inventory.Position==name]+position_size),2)
    inventory.Position_Size[inventory.Position==name] = inventory.Position_Size[inventory.Position==name]+position_size
    inventory.Position_Value[inventory.Position==name] = round(inventory.Position_Size[inventory.Position==name]*inventory.Value[inventory.Position==name],2)
    inventory.Gain_relative[inventory.Position==name] = round(100*inventory.Position_Value[inventory.Position==name]/(inventory.Position_Size[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name])-100,2)
    inventory.Gain_absolute[inventory.Position==name] = round(inventory.Position_Value[inventory.Position==name]-(inventory.Position_Size[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name]),2)

reset_all_positions()

for index, row in purchase_data.iterrows():
    add_buy_position(row['Item_Name'], row['Quantity'], row['Purchase_Price'])

# Update new percentages of the Portfolio
fonds_value = inventory['Position_Value'].sum()
inventory.Percentage = round(inventory.Position_Value/fonds_value*100,2)

#inventory.to_csv('Fonds_Position.csv')
inventory.to_csv('Fund_Positions_Test.csv')
