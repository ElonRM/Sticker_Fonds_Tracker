""" Updates the liquid_funds and amount_invested variable in
    dynamic_fund_values using the given input"""

import pandas as pd
import fund_variables as fv

NEWLY_INVESTED_FUNDS = 0
dynamic_variables = pd.read_csv(fv.DYNAMIC_VARIABLES,index_col=0)

dynamic_variables['Liquid_Funds'].iloc[0] += NEWLY_INVESTED_FUNDS
dynamic_variables['Amount_Invested'].iloc[0] += NEWLY_INVESTED_FUNDS
dynamic_variables.to_csv(fv.DYNAMIC_VARIABLES)
