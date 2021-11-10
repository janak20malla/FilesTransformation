import pandas as pd
import numpy as np
# import os
# import xlrd

# Reading the excel file, header chooses the header row.
data = pd.read_excel(r'path', header=[2, 3], index_col=None)

# Deleting the first empty column.
removeColumn = data.drop(data.columns[[0]], axis=1, inplace=True)
# data = data.drop([0], axis=0, inplace=True)                         # Deletes  a row permanently.

# Multi-index header (1st row: empty)
data.rename(columns={'Unnamed: 1_level_0': ' ', 'Unnamed: 2_level_0': ' '}, inplace=True)

# Converting the data into long format (keeping Fund and Investment column unchanged)
df1 = pd.melt(data, id_vars=[(' ', 'Fund'), (' ', 'Investment Name')])

# Renaming the columns names
new_col_list = ['Fund Name', 'Investment Name', 'DateAsOf', 'Variable_1', 'value']
df1 = df1.set_axis(new_col_list, axis='columns', inplace=False)

# Replace NaN values with 0.
df2 = df1.replace(np.NaN, 0, inplace=True)

# Remove the duplicate rows.
df2 = df1.drop_duplicates()

# Converting the Date Column to a specific format.
df2['DateAsOf'] = pd.to_datetime(df2['DateAsOf'], errors='coerce')
df2['DateAsOf'] = df2['DateAsOf'].dt.strftime('%m/%d/%Y')

# Separating the variable_1 column (containing 2 variable) into two different columns.
df2 = df2.pivot(index=['Fund Name', 'Investment Name', 'DateAsOf'], columns='Variable_1', values='value').reset_index().rename_axis(None, axis=1)

# Showing result without the index column.
print(df2.to_string(index=False))

# Saving the dataset.
df2.to_excel(r'path', header=True)
