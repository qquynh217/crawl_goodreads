import pandas as pd

data = pd.read_csv("data.csv",index_col="no")
# print(data.isna().sum()/data.shape[0])
null_rows = data.loc[data['rating'].isnull()]
print(null_rows)