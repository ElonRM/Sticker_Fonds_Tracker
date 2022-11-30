import pandas as pd

inventory = pd.read_csv('Fonds_Positions.csv', index_col=0)
purchase_data = pd.read_csv('dummy_buy_data.csv')

def add_buy_position(name, quantity, price):
    price=price*7.4 #currently because test data in euro
    inventory.Position_purchase_price[inventory.Position == name] = (inventory.Position_purchase_price[inventory.Position==name]*inventory.Quantity[inventory.Position==name]+price*quantity)/(inventory.Quantity[inventory.Position==name]+quantity)
    inventory.Quantity[inventory.Position==name] = inventory.Quantity[inventory.Position==name]+quantity
    inventory.Position_Value[inventory.Position==name] = inventory.Quantity[inventory.Position==name]*inventory.Value[inventory.Position==name]
    inventory.Gain_relative[inventory.Position==name] = round(100*inventory.Position_Value[inventory.Position==name]/(inventory.Quantity[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name])-100,2)
    inventory.Gain_absolute[inventory.Position==name] = round(inventory.Position_Value[inventory.Position==name]-(inventory.Quantity[inventory.Position==name]*inventory.Position_purchase_price[inventory.Position==name]),2)


for index, row in purchase_data.iterrows():
    add_buy_position(row['Position'], row['Quantity'], row['Position_purchase_price'])

# Update new percentages of the Portfolio
fonds_value = inventory['Position_Value'].sum()
inventory.Percentage = round(inventory.Position_Value/fonds_value,4)*100

#inventory.to_csv('Fonds_Position.csv')
inventory.to_csv('Fonds_Positions_Test.csv')