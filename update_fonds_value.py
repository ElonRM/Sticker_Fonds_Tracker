"""Updater for the value of each position and the complete Fund"""
import datetime
import pandas as pd

inventory = pd.read_csv('Fonds_Positions_Test.csv', index_col=0)

print(inventory[['Position', 'Percentage','Gain_relative', 'Gain_absolute']])
timestamp = datetime.datetime.now()
absolute_value = round(inventory['Position_Value'].sum(),2)
absolute_invested = round((inventory.Position_purchase_price*inventory.Quantity).sum(),2)
gain_relative = round(absolute_value/absolute_invested*100-100,2)
gain_absolute = absolute_value-absolute_invested

with open(r'value_history.csv', 'a', encoding='UTF-8') as fonds_value_history:
    fonds_value_history.write(
        f"\n{timestamp},{absolute_invested},{absolute_value},{gain_relative},{gain_relative}"
        )
