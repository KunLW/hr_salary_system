#%%
import pandas as pd
import numpy as np
import pprint
df = pd.read_csv('原始数据源表v20240511.csv', skiprows=2)
cleaned_column = [column for column in df.columns if column[0] != 'U']
df = df[cleaned_column]
pprint.pprint(df.columns)

# write txt file
with open('column.txt', 'w') as f:
    for column in df.columns:
        f.write(column + '\n')

std_df = pd.read_csv('Employee-2024-06-09.csv')

with open('std_column.txt', 'w') as f:
    for column in std_df.columns:
        f.write(column + '\n')

pprint.pprint(std_df.columns)

# %%
df.rename(columns={'姓名': '员工姓名',
                   '籍贯\n（省市/县）': '籍贯',
                   '政治\n面貌': '政治面貌',
                   '本公司社保开始缴纳日期': '社保始缴日',
                   '本公司公积金开始缴纳日期': '公积金始缴日',
                   '是否通过极简系统发放工资': '是否通过极简',
                   }, inplace=True)

#%%
print(df.head())

# write csv
df.to_csv('cleaned_employee.csv', index=False)




#%%
def create_num_map(old_df, new_df):
    num_map = {'姓名': [],
                        'old_num': [],
                        'new_num': []}
    for i, old_df in df.iterrows():
        for j, new_df in df.iterrows():
            if old_df['姓名'] == new_df['姓名']:
                # new_row = pd.DataFrame({'姓名': df_row['姓名'], 'old_num': df_row['编号'], 'new_num': df_row['编号']})
                num_map['姓名'].append(old_df['姓名'])
                num_map['old_num'].append(old_df['编号'])
                num_map['new_num'].append(new_df['编号'])
    return num_map

# %%
