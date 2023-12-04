import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time


def show_unique_values(df, col):
    print(f"Unique values of column '{col}':")
    for unique_value_n, unique_value in enumerate(df[col].unique(), start=1):
        print(f"{unique_value_n}. {unique_value}")
    print("")


def sanity_categorical_column(dataframe, subset):

    for column_n, column in enumerate(subset, start = 1):

        if dataframe[column].dtype == 'object' or dataframe[column].dtype == 'bool':
            number_of_unique_values = len(dataframe[column].unique())

            if number_of_unique_values <= 25:
                show_unique_values(df=dataframe, col=column)
                fig, ax = plt.subplots()
                order = dataframe[column].value_counts().index
                sns.countplot(y=column, data=dataframe, order=order, ax=ax).set_title(f"Categorical column: {column}")
                plt.tight_layout()
                plt.show()

            else:
                print(f"More than 25 unique observations ({number_of_unique_values} unique observations) in a column '{column}'. ")
                print("Print anyway? ('y' to print, 'n' to leave)")
                print_values = input("")

                if print_values == 'y':
                    show_unique_values(df=dataframe, col=column)

                elif print_values == 'n':
                    pass
                else:
                    print(f"Unknown value. Passing column '{column}'.")

            time.sleep(1.5)
        else:
            pass


def identifying_outliers(dataframe, column):
    quantile1 = dataframe[column].quantile(0.25)
    quantile3 = dataframe[column].quantile(0.75)
    iqr = quantile3 - quantile1
    threshold = iqr * 1.5
    lower_outliers = quantile1 - threshold
    upper_outliers = quantile3 + threshold
    outliers = dataframe[(dataframe[column] < lower_outliers) | (dataframe[column] > upper_outliers)]
    return outliers


def sanity_numerical_column(dataframe, subset):

    for column_n, column in enumerate(subset, start=1):

        if dataframe[column].dtype == 'float' or dataframe[column].dtype == 'int64':

            print(f"Descriptive Statistics of column '{column}':")
            print(dataframe[column].describe())

            fig, ax = plt.subplots()
            sns.histplot(x=column, data=dataframe, kde=True, ax=ax).set_title(f"Numerical column: {column}")
            plt.tight_layout()
            plt.show()

            outliers = identifying_outliers(dataframe, column)
            if not outliers.empty:
                print(f"WARNING: Column '{column}' has {len(outliers)} outliers.")
                print("Remove them? 'y' to remove, 'n' to leave")
                remove_na = input("")
                if remove_na == 'y':
                    dataframe_outliers_cleaned = dataframe.drop(outliers.index)
                elif remove_na == 'n':
                    dataframe_outliers_cleaned = dataframe
                else:
                    print("Unknown value. Skipping this column.")
                    dataframe_outliers_cleaned = dataframe
            else:
                dataframe_outliers_cleaned = dataframe

            time.sleep(1.5)
        else:
            dataframe_outliers_cleaned = dataframe

    return dataframe_outliers_cleaned


def sanity_date_column(dataframe, subset):

    for column in subset:

        if pd.api.types.is_datetime64_any_dtype(dataframe[column]):

            print(f"Column of type date: {column}")
            print(f"Latest date: {dataframe[column].dropna().max()}")
            print(f"Earliest date: {dataframe[column].dropna().min()}")

            fig, ax = plt.subplots()
            dataframe[column].hist(ax=ax)
            ax.set_title(f"Date column: {column}")
            plt.tight_layout()
            plt.show()
            time.sleep(2)


        else:
            pass


def data_sanity_check(df):

    print("""Do you want to perform a sanity check of the data?
'y' to check, 'n' to pass""")
    sanity_check = input("")
    if sanity_check == 'y':

        print(f"""Choose columns to check by writing their numbers: '1, 2, 5, 12'""")
        sanity_columns = df.columns.tolist()
        for i, column in enumerate(sanity_columns, start=1):
            if df[column].dtype == 'object' or df[column].dtype == 'bool':
                number_of_unique_values = len(df[column].unique())
                print(f"{i}. {column}. Type: {df[column].dtype}, unique values: {number_of_unique_values}")
            elif df[column].dtype == 'int64' or df[column].dtype == 'float':
                outliers = identifying_outliers(df, column)
                print(f"{i}. {column}. Type: {df[column].dtype}, number of outliers: {len(outliers)}")
            else:
                print(f"{i}. {column}. Type: {df[column].dtype}")
        columns_input = input("""Which columns to check:
""")

        columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
        columns_to_check = [sanity_columns[i] for i in columns_indexes]

        sanity_categorical_column(dataframe=df, subset=columns_to_check)
        dataframe_outliers_cleaned = sanity_numerical_column(dataframe=df, subset=columns_to_check)
        sanity_date_column(dataframe=df, subset=columns_to_check)

    elif sanity_check == 'n':
        dataframe_outliers_cleaned = df

    else:
        print("Unknown value. Leaving sanity check.")
        dataframe_outliers_cleaned = df

    return dataframe_outliers_cleaned


def data_sanity_step(df):
    df_corrected = data_sanity_check(df)
    print("")
    return df_corrected

