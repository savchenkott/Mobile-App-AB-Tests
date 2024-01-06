from cleaning.missing_values import data_na_cleaning_step
from cleaning.sanity_check import data_sanity_step
from cleaning.duplicates import duplicates_step
from cleaning.set_data_types import setting_data_types_step
from cleaning.custom_corrections import preliminary_dataset_corrections
from config.consts import *
import pandas as pd
import os
import analytics.revenue as rv
import analytics.stat_tests as an


def get_df_from_kaggle(username, dataset, filename, delete_from_directory=True):
    """
    Downloads specified cleaning from Kaggle to directory and returns it as cleaning.

    :param username: str, Kaggle username of file owner
    :param dataset: str, Kaggle cleaning name where the file is contained
    :param filename: str, the name of the file in the cleaning to download
    :param delete_from_directory: boolean, True - to delete the df file from directory
    :return: df
    """

    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()

    files_before = set(os.listdir('.'))

    dataset_to_download = f'{username}/{dataset}'
    api.dataset_download_files(dataset_to_download, path='.', unzip=True)
    files_after = set(os.listdir('.'))
    new_files = files_after - files_before

    df = pd.read_csv(filename)
    for file in new_files:
        if file != filename:
            os.remove(file)

    if delete_from_directory:
        os.remove(filename)

    return df


def df_basic_cleaning(df):

    df_corrected = preliminary_dataset_corrections(df)
    df_with_types = setting_data_types_step(df=df_corrected)
    df_sanity_checked = data_sanity_step(df=df_with_types)
    df_duplicates_cleaned = duplicates_step(df=df_sanity_checked)
    df_na_cleaned = data_na_cleaning_step(df=df_duplicates_cleaned)

    print("Data cleaning process done")

    return df_na_cleaned


# p_value = an.one_way_anova_for_df(df=df_cleaned, category_column='Subscription Type',
#                                group_of_interest=['Basic', 'Premium', 'Standard'], numerical_column='Period Revenue')
# print(rv.arpu_calculation(df=df_cleaned, revenue='Period Revenue', user_id='User ID'))
# print(rv.churn_rate_calculation(df=df_cleaned, user_id='User ID', payment='Payment Date'))
# print(rv.ltv_calculation(df=df_cleaned, revenue='Period Revenue', payment='Payment Date', user_id='User ID'))
