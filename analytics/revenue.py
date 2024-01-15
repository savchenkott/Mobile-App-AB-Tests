# TODO: Correct funcitons docs
from dateutil.relativedelta import relativedelta
import pandas as pd


def churn_rate_one_period(df, date_column, user_id):
    total_customers = df[user_id].nunique()
    latest_subscription = df[date_column].max() - relativedelta(days=1)

    not_churned_customers = df[df['Last Day'] > latest_subscription][user_id].nunique()
    churned_customers = total_customers - not_churned_customers

    churn_rate = round((churned_customers / total_customers) * 100, 2)
    return churn_rate


def churn_rate_two_periods(df, date_column, user_id, date_split, timespan):

    split_timespan = timespan.split(" ")

    if "months" in split_timespan:
        number_of_months = int(split_timespan[0])
        end_date = date_split + relativedelta(months=number_of_months)
    elif "days" in split_timespan:
        number_of_days = int(split_timespan[0])
        end_date = date_split + relativedelta(days=number_of_days)
    elif "years" in split_timespan:
        number_of_years = int(split_timespan[0])
        end_date = date_split + relativedelta(years=number_of_years)
    else:
        raise ValueError("Invalid timespan.")

    df1 = df[(df[date_column] < date_split) & (df["Last Day"] >= date_split)]
    start_users = df1[user_id].unique()

    df3 = df[df[user_id].isin(start_users) & (df[date_column] < end_date) & (df["Last Day"] >= end_date)]
    end_users = df3[user_id].unique()

    customers_before = len(start_users)
    not_churned_customers = len(end_users)
    churned_customers = customers_before - not_churned_customers

    if customers_before > 0:
        churn_rate = round(((churned_customers / customers_before) * 100), 2)
    else:
        # print("DIVISION BY ZERO")
        churn_rate = 0

    return churn_rate


def churn_rate_calculation(df, user_id, plan_duration, date_column, date_split=None, timespan='whole'):
    """
    This function calculates the churn rate for a given DataFrame of subscription data.
    The churn rate is the percentage of subscribers who stop their subscriptions within a certain time period.

    :param date_split:
    :param df: The input DataFrame containing the subscription data.
    :param user_id: The column name in the DataFrame that represents unique user identifiers.
    :param date_column: The column name in the DataFrame that represents the payment dates.
    :param plan_duration: The column name in the DatFrame that represents the plan duration in format 'x months'.
    :param date_column: (optional) The column name in the DataFrame that represents the date.
    If not provided, the function will use the entire DataFrame.
    :param timespan: (optional) The timespan for which to calculate the churn rate.
    It should be in the format of [YYYY-MM-DD, YYYY-MM-DD, YYYY-MM-DD], or ‘whole’ for the entire DataFrame. The default is ‘whole’.
    :return: calculated churn rate.
    """

    df.loc[:, 'Duration'] = df.loc[:, plan_duration].apply(lambda x: int(x.split(" ")[0]))
    df.loc[:, 'Last Day'] = df.apply(lambda row: row[date_column] + relativedelta(months=int(row['Duration'])), axis=1)
    df.loc[:, 'Last Day'] = pd.to_datetime(df['Last Day'])

    if timespan == "whole":
        churn_rate = churn_rate_one_period(df=df, date_column=date_column, user_id=user_id)
    else:
        churn_rate = churn_rate_two_periods(df=df, date_column=date_column, user_id=user_id, date_split=date_split,
                                            timespan=timespan)

    return churn_rate


def arpu_calculation(df, revenue, user_id, date_split=None, date_column=None, timespan='whole'):
    """
    This function calculates the Average Revenue Per User for a given DataFrame of subscription data.
    ARPU is defined as the total revenue divided by the number of subscribers.

    :param date_split:
    :param df: The input DataFrame containing the subscription data.
    :param revenue: The column name in the DataFrame that represents the revenue.
    :param user_id: The column name in the DataFrame that represents unique user identifiers.
    :param date_column: (optional) The column name in the DataFrame that represents the date.
    If not provided, the function will use the entire DataFrame.
    :param timespan: (optional) The timespan for which to calculate the ARPU.
    It can be in the format of ‘x days’, ‘x months’, ‘x years’, or ‘whole’ for the entire DataFrame. The default is ‘whole’.
    :return: calculated ARPU.
    """

    split_timespan = timespan.split(" ")

    if date_column:
        if "months" in split_timespan:
            number_of_months = int(split_timespan[0])
            start_date = date_split - relativedelta(months=number_of_months)
            filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= date_split)]
        elif "days" in split_timespan:
            number_of_days = int(split_timespan[0])
            start_date = date_split - relativedelta(days=number_of_days)
            filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= date_split)]
        elif "years" in split_timespan:
            number_of_years = int(split_timespan[0])
            start_date = date_split - relativedelta(years=number_of_years)
            filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= date_split)]
        elif timespan == "whole":
            filtered_df = df
        else:
            raise ValueError("Invalid unit. Supported units are 'x days', 'x months', 'x years', and 'whole'")
    else:
        filtered_df = df

    arpu = filtered_df[revenue].agg('sum') / len(filtered_df[user_id].unique())

    return arpu


def ltv_calculation(df, revenue, plan_duration, user_id, date_column, timespan='whole', date_split=None):
    """
    This function calculates the Lifetime Value (LTV) for a given DataFrame of subscription data.
    LTV is a prediction of the net profit attributed to the entire future relationship with a customer.

    :param date_split:
    :param plan_duration:
    :param df: The input DataFrame containing the subscription data.
    :param revenue: The column name in the DataFrame that represents the revenue.
    :param user_id: The column name in the DataFrame that represents unique user identifiers.
    :param date_column: (optional) The column name in the DataFrame that represents the date.
    If not provided, the function will use the entire DataFrame.
    :param timespan: (optional) The timespan for which to calculate the LTV.
    It can be in the format of ‘x days’, ‘x months’, ‘x years’, or ‘whole’ for the entire DataFrame. The default is ‘whole’.
    :return: calculated LTV.
    """

    churn_rate = churn_rate_calculation(df=df, user_id=user_id, plan_duration=plan_duration, date_split=date_split,
                                        date_column=date_column, timespan=timespan) * 0.01
    arpu = arpu_calculation(df=df, revenue=revenue, user_id=user_id, date_split=date_split, date_column=date_column,
                            timespan=timespan)

    ltv = arpu / churn_rate

    return ltv
