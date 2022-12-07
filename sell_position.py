""" Adds Functionality to sell a specific amout of a position,
 calculates the selling fees and adds the gained money to liquid funds"""

import pandas as pd
import fund_variables as fv

def sell_position(item_id, quantity):
    """ sells the item Using item_id and updates available liquid funds """

    new_position_size = inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] - quantity
    item_value = inventory.loc[inventory.Item_ID == item_id, 'Value']

    inventory.loc[inventory.Item_ID == item_id, 'Position_Size'] = new_position_size
    inventory.loc[inventory.Item_ID == item_id, 'Position_Value'] = new_position_size*item_value
    inventory.loc[inventory.Item_ID == item_id, 'Gain_absolute'] = new_position_size*(item_value-inventory.loc[inventory.Item_ID == item_id, 'Position_purchase_price'])


if __name__ == '__main__':
    inventory = pd.read_csv(fv.FUND_FILENAME, index_col=0)
    dynamic_variables = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0)
    sell_data = pd.read_csv(fv.SELL_DATA)

    total_sell_value = round(sum(round(int(sell_data.Sell_Price*100*0.975)/100*sell_data.Quantity,2)),2)
    dynamic_variables['Liquid_Funds'].iloc[0] += total_sell_value

    liquid_funds = dynamic_variables.iloc[0]['Liquid_Funds']
    for index, row in sell_data.iterrows():
        sell_position(row['Item_ID'], row['Quantity'])

    fund_value = inventory['Position_Value'].sum()+liquid_funds
    inventory.Percentage = round(inventory.Position_Value/fund_value*100,2)

    dynamic_variables.to_csv(fv.DYNAMIC_VARIABLES)
    inventory.to_csv(fv.FUND_FILENAME)
