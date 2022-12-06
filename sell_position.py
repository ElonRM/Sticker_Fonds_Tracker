""" Adds Functionality to sell a specific amout of a position,
 calculates the selling fees and adds the gained money to liquid funds"""

import pandas as pd
import numpy as np

FILENAME = 'Fund_Positions_Test.csv'
LIQUID_FUNDS = 'Liquid_Funds.csv'
ITEM_ID = 875837
QUANTITY = 100
PRICE = 4.89

def sell_position(item_id, quantity, price):
    """ sells the item Using item_id and updates available liquid funds """
    #inventory.Position_Size[inventory.Item_ID == item_id] -= quantity
    #print(inventory.loc[inventory.Item_ID == item_id, 'Position_Size'], inventory.loc[inventory.Item_ID == item_id, 'Position_Value'])
    inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] -= quantity
    inventory.loc[inventory.Item_ID == item_id, 'Position_Value'] = inventory.loc[inventory.Item_ID == item_id, 'Position_Size']*inventory.loc[inventory.Item_ID == item_id, 'Value']
    #print(inventory.loc[inventory.Item_ID == item_id, 'Position_Size'], inventory.loc[inventory.Item_ID == item_id, 'Position_Value'])
    gained_funds = int(price*100*0.975)/100*quantity
    funds.Liquid_Funds += gained_funds
    funds.to_csv(LIQUID_FUNDS)
    inventory.to_csv(FILENAME)


if __name__ == '__main__':
    inventory = pd.read_csv(FILENAME, index_col=0)
    funds = pd.read_csv(LIQUID_FUNDS, index_col=0)
    print(funds)
    sell_position(ITEM_ID, QUANTITY, PRICE)
    print(funds)