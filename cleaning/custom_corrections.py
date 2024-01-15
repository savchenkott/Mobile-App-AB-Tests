import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import analytics.revenue as rv
import cleaning.duplicates as dups

random_state = 1


def mask_creation(df, column_to_filter, value_to_filter, index_to_change, percentage, column_to_change, value_to_change):
    filtered_df = df[df[column_to_filter] == value_to_filter]
    mask = filtered_df.sample(frac=(index_to_change * percentage), random_state=1).index
    df.loc[mask, column_to_change] = value_to_change


def preliminary_dataset_corrections(df, random_state=1):

    df['Last Payment Date'] = pd.to_datetime(df['Last Payment Date'])
    df['Join Date'] = pd.to_datetime(df['Join Date'])
    df = df.rename(columns={'Last Payment Date': 'Payment Date'})

    mask1 = df.sample(frac=0.35, random_state=1).index
    df.loc[mask1, 'Plan Duration'] = '1 Month'
    remaining_indices = df.index.difference(mask1)
    mask2 = df.loc[remaining_indices].sample(frac=0.6, random_state=1).index
    df.loc[mask2, 'Plan Duration'] = '6 Months'
    remaining_indices2 = df.index.difference(mask1.union(mask2))
    mask3 = remaining_indices2
    df.loc[mask3, 'Plan Duration'] = '12 Months'

    mask1 = df.sample(frac=0.65, random_state=1).index
    df.loc[mask1, 'Subscription Type'] = 'Basic'
    remaining_indices = df.index.difference(mask1)
    mask2 = df.loc[remaining_indices].sample(frac=0.6, random_state=1).index
    df.loc[mask2, 'Subscription Type'] = 'Standard'
    remaining_indices2 = df.index.difference(mask1.union(mask2))
    mask3 = remaining_indices2
    df.loc[mask3, 'Subscription Type'] = 'Premium'

    np.random.seed(random_state)
    device_order = ['SmartTV', 'Laptop', 'Tablet', 'Smartphone']
    country_order = ['United States', 'United Kingdom', 'Canada', 'Australia', 'France', 'Mexico', 'Germany', 'Italy',
                     'Spain', 'Mexico']

    for d, device in enumerate(device_order, start=1):
        mask_creation(df=df,
                      column_to_filter='Device',
                      value_to_filter=device,
                      index_to_change=d,
                      percentage=0.018,
                      column_to_change='Plan Duration',
                      value_to_change='6 Month')
        mask_creation(df=df,
                      column_to_filter='Device',
                      value_to_filter=device,
                      index_to_change=d,
                      percentage=0.04,
                      column_to_change='Subscription Type',
                      value_to_change='Basic')

    for d, device in enumerate(reversed(device_order), start=0):
        mask_creation(
            df=df,
            column_to_filter='Device',
            value_to_filter=device,
            index_to_change=d,
            percentage=0.12**d,
            column_to_change='Plan Duration',
            value_to_change='12 Month'
        )

    for c, country in enumerate((country_order), start=1):
        mask_creation(df=df,
                      column_to_filter='Country',
                      value_to_filter=country,
                      index_to_change=c,
                      percentage=0.15**c,
                      column_to_change='Subscription Type',
                      value_to_change='Premium')
        mask_creation(df=df,
                      column_to_filter='Country',
                      value_to_filter=country,
                      index_to_change=c,
                      percentage=0.15**c,
                      column_to_change='Plan Duration',
                      value_to_change='12 Months')

    for c, country in enumerate(reversed(country_order), start=1):
        mask_creation(df=df, column_to_filter='Country', value_to_filter=country, index_to_change=c, percentage=0.015,
                      column_to_change='Subscription Type', value_to_change='Basic')
        mask_creation(df=df, column_to_filter='Country', value_to_filter=country, index_to_change=c,
                      percentage=0.01, column_to_change='Plan Duration', value_to_change='1 Month')

    extension = df.sample(n=8000, replace=True, random_state=random_state).sort_values("User ID").reset_index(drop=True)
    extension_cop = extension.copy()
    max_date = df['Payment Date'].max() + relativedelta(days=24)
    indices_to_drop = []

    for u, user in enumerate(extension['User ID'].unique()):
        sorting = extension[extension['User ID'] == user]
        for r, (index, row) in enumerate(sorting.iterrows()):
            sorting_new = extension_cop[extension_cop['User ID'] == user]
            if r == 0:
                duration = int(row['Plan Duration'].split(" ")[0])
                new_date = row['Payment Date'] + relativedelta(months=duration)
                if new_date <= max_date and new_date not in sorting_new['Payment Date'].values:
                    extension_cop.at[sorting_new.index[r], 'Payment Date'] = new_date
                    sorting_new.at[sorting_new.index[r], 'Payment Date'] = new_date
                else:
                    indices_to_drop.append(sorting_new.index[r])
                if u == 1:
                    mask4 = np.random.rand(len(extension_cop)) < 0.04
                    extension_cop.loc[mask4, 'Plan Duration'] = np.random.choice(['1 Month', '6 Months', '12 Months'],
                                                                                 size=mask4.sum())
            else:
                previous_row = sorting_new.iloc[(r - 1)]
                duration = int(previous_row['Plan Duration'].split(" ")[0])
                new_date = previous_row['Payment Date'] + relativedelta(months=duration)
                if new_date <= max_date and new_date not in sorting_new['Payment Date'].values:
                    extension_cop.at[sorting_new.index[r], 'Payment Date'] = new_date
                    sorting_new.at[sorting_new.index[r], 'Payment Date'] = new_date

    extension_cop = extension_cop.drop(indices_to_drop)

    mask5 = np.random.rand(len(extension_cop)) < 0.04
    extension_cop.loc[mask5, 'Subscription Type'] = np.random.choice(['Basic', 'Premium', 'Standard'], size=mask5.sum())

    df_extended = pd.concat([df, extension_cop])

    df_extended.rename(columns={'Monthly Revenue': 'Period Revenue'}, inplace=True)

    df_extended['Period Revenue'] = df_extended['Period Revenue'].astype(float)
    df_extended.loc[df_extended['Subscription Type'] == 'Basic', 'Period Revenue'] = 4
    df_extended.loc[df_extended['Subscription Type'] == 'Standard', 'Period Revenue'] = 6.2
    df_extended.loc[df_extended['Subscription Type'] == 'Premium', 'Period Revenue'] = 7.5

    df_extended.loc[df_extended['Plan Duration'] == '6 Months', 'Period Revenue'] *= 4.2
    df_extended.loc[df_extended['Plan Duration'] == '12 Months', 'Period Revenue'] *= 8.33

    return df_extended


# df1 = pd.DataFrame({
#     'User ID': ['user1', 'user2', 'user3'],
#     'Subscription Type': ['Basic', 'Basic', 'Premium'],
#     'Device': ['SmartTV', 'Laptop', 'Tablet'],
#     'Gender': ['Male', 'Female', 'Male'],
#     'Country': ['Brazil', 'Italy', 'Spain'],
#     'Join Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
#     'Plan Duration': ['1 Months', '1 Months', '1 Months'],
#     'Last Payment Date': ['2023-01-01', '2023-02-01', '2024-02-01'],
#     'Monthly Revenue': [23, 23, 43]
# })
# print("Before:")
# print(df1)
# df2 = preliminary_dataset_corrections(df1)
# df3 = dups.duplicates_step(df2)
# print("After:")
# print(df3)
#
# print(rv.churn_rate_calculation(df=df3, user_id='User ID', plan_duration='Plan Duration',
#                                 date_column='Payment Date', timespan='whole'))
# print((rv.arpu_calculation(df=df3, user_id='User ID', revenue='Period Revenue', date_column='Payment Date')))
# print(rv.ltv_calculation(df=df3, user_id='User ID', plan_duration='Plan Duration', date_column='Payment Date',
#                          revenue='Period Revenue', timespan='whole'))
#
# churn_rate_df = pd.DataFrame(columns=['Date', 'Churn'])
# df3['YearMonth'] = df3['Payment Date'].dt.to_period('M')
# df3['YearMonth'] = df3['YearMonth'].dt.to_timestamp()
#
# for d, date in enumerate(df3['YearMonth'].unique(), start=0):
#
#     print(date)
#     churn = rv.churn_rate_calculation(df=df3, user_id='User ID', plan_duration='Plan Duration', date_split=date,
#                                         date_column='Payment Date', timespan='1 months')
#     new_row = {'Date': date, 'Churn': churn}
#     print(churn)
#     churn_rate_df = pd.concat([churn_rate_df, pd.DataFrame([new_row])], ignore_index=True)
#
# print(rv.churn_rate_calculation(df=df3, user_id='User ID', plan_duration='Plan Duration', date_column='Payment Date',
#                                 timespan='whole'))