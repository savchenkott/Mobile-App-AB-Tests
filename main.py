import dataset_download as dd
from config.consts import *
import analytics.revenue as rv

def main(path, overwrite=True, cleaning=True):

    df = dd.get_df_from_kaggle(username=DEFAULT_USERNAME, dataset=DEFAULT_DATASET, filename=DEFAULT_FILE)
    if cleaning == True:
        df_cleaned = dd.df_basic_cleaning(df=df)
    else:
        df_cleaned = df

    if overwrite == True:
        df_cleaned.to_csv(path)
    else:
        df_cleaned.to_csv(path, mode='x')


if __name__ == "__main__":
    main(path='netflix.csv')

