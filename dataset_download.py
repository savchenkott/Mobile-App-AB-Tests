from dataset.missing_values import data_na_cleaning_step
from dataset.sanity_check import data_sanity_step
from dataset.duplicates import duplicates_step
from dataset.set_data_types import setting_data_types_step
from dataset.custom_corrections import custom_sanity_correction, custom_na_correction, custom_dtypes_correction,\
    duplicates_correction
from config.consts import *
import pandas as pd
import zipfile
import os


def get_df_from_kaggle(username, dataset, filename, delete_from_directory=True):
    """
    Downloads specified dataset from Kaggle to directory and returns it as dataset.
    :param username: str, Kaggle username of file owner
    :param dataset: str, Kaggle dataset name where the file is contained
    :param filename: str, the name of the file in the dataset to download
    :param delete_from_directory: boolean, True - to delete the file from directory
    :return: df
    """
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    dataset_to_download = f'{username}/{dataset}'
    api.dataset_download_file(dataset_to_download, file_name=filename, path='.')
    with zipfile.ZipFile(f'{filename}.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove(f'{filename}.zip')
    df = pd.read_csv(filename)
    if delete_from_directory:
        os.remove(f'{filename}')
    return df


df = get_df_from_kaggle(username=DEFAULT_USERNAME, dataset=DEFAULT_DATASET, filename=DEFAULT_FILE)


data = pd.read_excel('/Users/tanya/Desktop/Универ/KSE магистратура/Term II/S&E II/Group E. New York Airbnb.xlsx')


def df_basic_cleaning(df):

    df_dtypes_corrected = custom_dtypes_correction(df)
    df_with_types = setting_data_types_step(df=df_dtypes_corrected)

    df_sanity_corrected = custom_sanity_correction(df_with_types)
    df_sanity_checked = data_sanity_step(df=df_sanity_corrected)

    df_duplicates_corrected = duplicates_correction(df_sanity_checked)
    df_duplicates_cleaned = duplicates_step(df=df_duplicates_corrected)

    df_na_corrected = custom_na_correction(df_duplicates_cleaned)
    df_na_cleaned = data_na_cleaning_step(df=df_na_corrected)

    print("Data cleaning process done")

    return df_na_cleaned


df_cleaned = df_basic_cleaning(df=df)
