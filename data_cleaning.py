""" Used for Cleaning Up Variables, especially DataFrames during development"""
import pandas as pd
import fund_variables as fv

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