from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from pandas import DateOffset


def churn_rate_calculation(df, user_id, payment, date=None, timespan='whole'):

    total_customers = (df.nunique()[user_id])
    latest_subscription = df[payment].max()

    df['Duration'] = df['Plan Duration'].apply(lambda x: int(x.split(" ")[0]))
    df['Last Day'] = df[payment] + df['Duration'].apply(lambda x: pd.DateOffset(months=x))
    df['Last Day'] = pd.to_datetime(df['Last Day'])
    not_churned_customers = (df[df['Last Day'] > latest_subscription].nunique()[user_id])
    churned_customers = total_customers - not_churned_customers

    churn_rate = round(((churned_customers / total_customers) * 100), 2)

    return churn_rate



def arpu_calculation(df, revenue, user_id, date=None, timespan='whole'):

    split_timespan = timespan.split(" ")

    if date:
        if "months" in split_timespan:
            number_of_months = int(split_timespan[0])
            start_date = df['date'].max() - relativedelta(months=number_of_months)
            filtered_df = df[(df['date'] >= start_date) & (df['date'] <= df['date'].max())]
        elif "days" in split_timespan:
            number_of_days = int(split_timespan[0])
            start_date = max(df[date]) - relativedelta(days=number_of_days)
            filtered_df = df[(df['date'] >= start_date) & (df['date'] <= df['date'].max())]
        elif "years" in split_timespan:
            number_of_years = int(split_timespan[0])
            start_date = max(df[date]) - relativedelta(years=number_of_years)
            filtered_df = df[(df['date'] >= start_date) & (df['date'] <= df['date'].max())]
        elif timespan == "whole":
            filtered_df = df
        else:
            raise ValueError("Invalid unit. Supported units are 'x days', 'x months', 'x years', and 'whole'")
    else:
        filtered_df = df

    arpu = filtered_df[revenue].agg('sum') / len(filtered_df[user_id].unique())

    return arpu


# def ltv_calculation():
#
#     return ltv