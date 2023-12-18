import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta


def preliminary_dataset_corrections(df, random_state=27):

    df['Last Payment Date'] = pd.to_datetime(df['Last Payment Date'])
    df['Join Date'] = pd.to_datetime(df['Join Date'])
    df = df.rename(columns={'Last Payment Date': 'Payment Date'})

    np.random.seed(random_state)
    mask1 = np.random.rand(len(df)) < 0.1
    df.loc[mask1, 'Plan Duration'] = '1 Months'
    mask2 = (np.random.rand(len(df)) < 0.5) & ~mask1
    df.loc[mask2, 'Plan Duration'] = '6 Months'
    mask3 = ~(mask1 | mask2)
    df.loc[mask3, 'Plan Duration'] = '12 Months'

    mask1 = np.random.rand(len(df)) < 0.9
    df.loc[mask1, 'Subscription Type'] = 'Basic'
    mask2 = (np.random.rand(len(df)) < 0.95) & ~mask1
    df.loc[mask2, 'Subscription Type'] = 'Standard'
    mask3 = ~(mask1 | mask2)
    df.loc[mask3, 'Subscription Type'] = 'Premium'

    extension = df.sample(n=6000, replace=True, random_state=random_state).sort_values("User ID").reset_index(drop=True)
    extension_cop = extension.copy()
    max_date = df['Payment Date'].max()
    indices_to_drop = []

    for u, user in enumerate(extension['User ID'].unique()):
        sorting = extension[extension['User ID'] == user]
        for r, (index, row) in enumerate(sorting.iterrows()):
            if r == 0:
                sorting_new = extension_cop[extension_cop['User ID'] == user]
                duration = int(row['Plan Duration'].split(" ")[0])
                new_date = row['Payment Date'] + relativedelta(months=duration)

                if new_date <= max_date:
                    extension_cop.at[row.name, 'Payment Date'] = new_date
                    sorting_new.at[row.name, 'Payment Date'] = new_date
                else:
                    indices_to_drop.append(row.name)

                if u == 1:
                    mask4 = np.random.rand(len(extension_cop)) < 0.08
                    extension_cop.loc[mask4, 'Plan Duration'] = np.random.choice(['1 Months', '6 Months', '12 Months'], size=mask4.sum())
                else:
                    pass
            else:
                sorting_new = extension_cop[extension_cop['User ID'] == user]
                previous_row = sorting_new.iloc[(r-1)]
                current_row = sorting_new.iloc[r]
                duration = int(previous_row['Plan Duration'].split(" ")[0])
                new_date = previous_row['Payment Date'] + relativedelta(months=duration)
                if new_date <= max_date:
                    extension_cop.at[current_row.name, 'Payment Date'] = new_date
                    sorting_new.at[current_row.name, 'Payment Date'] = new_date
                else:
                    indices_to_drop.append(row.name)

    extension_cop.drop(indices_to_drop, inplace=True)
    mask5 = np.random.rand(len(extension_cop)) < 0.08
    extension_cop.loc[mask5, 'Subscription Type'] = np.random.choice(['Basic', 'Premium', 'Standard'], size=mask5.sum())

    df_extended = pd.concat([df, extension_cop])

    df_extended.rename(columns={'Monthly Revenue': 'Period Revenue'}, inplace=True)

    df_extended['Period Revenue'] = df_extended['Period Revenue'].astype(float)
    df_extended.loc[df_extended['Subscription Type'] == 'Basic', 'Period Revenue'] = 3
    df_extended.loc[df_extended['Subscription Type'] == 'Standard', 'Period Revenue'] = 4.2
    df_extended.loc[df_extended['Subscription Type'] == 'Premium', 'Period Revenue'] = 7.5

    df_extended.loc[df_extended['Plan Duration'] == '6 Months', 'Period Revenue'] *= 4.2
    df_extended.loc[df_extended['Plan Duration'] == '12 Months', 'Period Revenue'] *= 8.33

    return df_extended



# df1 = pd.DataFrame({
#     'User ID': ['user1', 'user2', 'user3'],
#     'Subscription Type': ['Basic', 'Basic', 'Premium'],
#     'Last Payment Date': ['2023-01-01', '2023-02-01', '2024-02-01'],
#     'Join Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
#     'Plan Duration': ['1 Months', '1 Months', '1 Months'],
#     'Monthly Revenue': [23, 23, 43]
# })
# print("Before:\n", df1)
# df2 = preliminary_dataset_corrections(df1)
# print("After:\n", df2)