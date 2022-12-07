"""Adding new Purchases to the Fund using a csv file"""

import datetime
import pandas as pd
import fund_variables as fv

# TODO  # pylint: disable=fixme
# If bought item doesnt yet exist in the Fund, add it to the fund

def reset_all_positions():
    """Sets all Position_Sizes to 0"""
    inventory.Position_Size = 0
    inventory.Position_Value = 0

def add_buy_position(item_id, quantity, price):
    """Updates purchase price, Position Size, Position Value of a 
    newly bought item in the Fund"""
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

inventory = pd.read_csv(fv.FUND_FILENAME, index_col=0)
purchase_data = pd.read_csv(fv.PURCHASE_DATA)
buy_order_history = pd.read_csv(fv.BUY_ORDER_HISTORY, index_col=0)
dynamic_variables = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0)
#liquid_funds = pd.read_csv(fv.LIQUID_FUNDS, index_col=0).iloc[0]['Liquid_Funds']

#reset_all_positions()

# Updates the Fund Values for each bought Item
for index, row in purchase_data.iterrows():
    add_buy_position(row['Item_ID'], row['Quantity'], row['Purchase_Price'])

# Adding the purchase to the purchase history
total_order_price = round(sum(purchase_data.Quantity*purchase_data.Purchase_Price),2)
buy_order_history = buy_order_history.append({'Date': datetime.datetime.now().date(),
                                        'Item_IDs': purchase_data.Item_ID.to_list(),
                                        'Prices': purchase_data.Purchase_Price.to_list(),
                                        'Quantities': purchase_data.Quantity.to_list(),
                                        'Total_Order_Price': total_order_price},
                                    ignore_index = True
                                    )

# Updates the Value of liquid_funds
dynamic_variables['Liquid_Funds'].iloc[0] -= total_order_price
dynamic_variables.to_csv(fv.DYNAMIC_VARIABLES)

liquid_funds = dynamic_variables.iloc[0]['Liquid_Funds']
# Updating the percentages of the Portfolio
fund_value = inventory['Position_Value'].sum()
inventory.Percentage = round(inventory.Position_Value/(fund_value+liquid_funds)*100,2)

inventory.to_csv(fv.FUND_FILENAME)
buy_order_history.to_csv(fv.BUY_ORDER_HISTORY)
