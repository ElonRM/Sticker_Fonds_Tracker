""" Used for Cleaning Up Variables, especially DataFrames during development"""
import pandas as pd
import fund_variables as fv
import update_fund_value

FILENAME = 'Data/Fund_Positions_Test.csv'

df = pd.read_csv(fv.FUND_FILENAME, index_col=0)

# df["Item_ID"] = df.URL.apply(lambda x: x.split("goods/")[1].split(["?"][0])[0])

# df = df.drop('URL', axis=1)
# print(df.columns)
# df.to_csv("Fund_Positions_Test.csv")

#df[['Position', 'Percentage']].to_csv('planned_percentages.csv')

#df.drop('Rating', axis=1, inplace=True)
#df.Item_ID = df.Item_ID.apply(lambda x: int(x))
#df.to_csv('Fund_Positions_Test.csv')
#print(df.columns)
#print(df.dtypes)

update_fund_value.save_fund_value(df, liquid_funds = pd.read_csv(fv.DYNAMIC_VARIABLES).iloc[0]['Liquid_Funds'])
# dv = pd.read_csv(fv.DYNAMIC_VARIABLES)
# print(dv.loc[0, 'Liquid_Funds'])
# order_price = 1000
# dv.loc[0, 'Liquid_Funds'] = round(dv.loc[0, 'Liquid_Funds'] - order_price,2)

# liquid_funds = dv.loc[0,'Liquid_Funds']
# print(liquid_funds)

# buy_order_history = pd.read_csv(fv.BUY_ORDER_HISTORY, index_col=0)
# purchase_data = pd.read_csv(fv.PURCHASE_DATA)

# order_price = 2000

# import datetime
# buy_order_history = pd.concat([buy_order_history,
#                                 pd.DataFrame({'Date': datetime.datetime.now().date(),
#                                             'Item_IDs': purchase_data.Item_ID.to_list(),
#                                             'Prices': purchase_data.Purchase_Price.to_list(),
#                                             'Quantities': purchase_data.Quantity.to_list(),
#                                             'Total_Order_Price': order_price})],
#                                 ignore_index=True
#                                 )
# print(purchase_data.Quantity.to_list())
# print(buy_order_history)
# #buy_order_history.to_csv(fv.BUY_ORDER_HISTORY)

"""
ropz 3
max 1
navi antwerp 10
g2 holo antwerp 2
furia antwerp 1
pain 10
entropiq 7

"""