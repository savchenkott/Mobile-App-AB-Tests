import pandas as pd


def fill_na_values_numeric_column(dataframe, column_name):
    df = dataframe.copy()
    column = column_name
    fill = input(f"""For column '{column}' (type integer/float) choose the replacement type: 'mean', 'median', 'mode', 'forward', 'backward'.
    Format:                                                'mean'
    Or enter custom value:                                 '0'
    Set limit to replace only first n missing values:      'median; limit = 3'
    Enter 'skip' to leave the column values as they are:   'skip'
    """)
    if ";" in fill:
        fill_type = (fill.split(";", 1)[0])
        fill_limit = int(fill.split(";", 1)[1].replace(" ", "").replace("limit=", ""))
        if str(fill).strip() == 'mean':
            df[column] = df[column].fillna(df[column].mean(), limit=fill_limit)
        elif str(fill).strip() == 'median':
            df[column] = df[column].fillna(df[column].median(), limit=fill_limit)
        elif str(fill).strip() == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0], limit=fill_limit)
        elif str(fill).strip() == 'forward':
            df[column] = df[column].fillna(method='ffill', limit=fill_limit)
        elif str(fill).strip() == 'backward':
            df[column] = df[column].fillna(method='bfill', limit=fill_limit)
        else:
            df[column] = df[column].fillna(fill_type, limit=fill_limit)
    elif fill == 'skip':
        pass
    else:
        if str(fill).strip() == 'mean':
            df[column] = df[column].fillna(df[column].mean())
        elif str(fill).strip() == 'median':
            df[column] = df[column].fillna(df[column].median())
        elif str(fill).strip() == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        elif str(fill).strip() == 'forward':
            df[column] = df[column].fillna(method='ffill')
        elif str(fill).strip() == 'backward':
            df[column] = df[column].fillna(method='bfill')
        else:
            df[column] = df[column].fillna(fill)
    print(" ")
    return df


def fill_na_values_categorical_column(dataframe, column_name):
    df = dataframe.copy()
    column = column_name
    fill = input(f"""For column '{column}' (type object, boolean, string or date) choose the replacement type: 'mode', 'forward', 'backward'.
    Format:                                                'mode'
    Or enter custom value:                                 '0'
    Set limit to replace only first n missing values:      'forward; limit = 3'
    Enter 'skip' to leave the column values as they are:   'skip'
    """)
    if ";" in fill:
        fill_type = fill.split(";", 1)[0]
        fill_limit = int(fill.split(";", 1)[1].replace(" ", "").replace("limit=", ""))
        if str(fill_type).strip() == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0], limit=fill_limit)
        elif str(fill_type).strip() == 'forward':
            df[column] = df[column].fillna(method='ffill', limit=fill_limit)
        elif str(fill_type).strip() == 'backward':
            df[column] = df[column].fillna(method='bfill', limit=fill_limit)
        else:
            df[column] = df[column].fillna(fill_type, limit=fill_limit)
    elif fill == 'skip':
        pass
    else:
        if str(fill).strip() == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        elif str(fill).strip() == 'forward':
            df[column] = df[column].fillna(method='ffill')
        elif str(fill).strip() == 'backward':
            df[column] = df[column].fillna(method='bfill')
        else:
            df[column] = df[column].fillna(fill)
    print(" ")
    return df


def fill_missing_values(dataframe):
    df = dataframe.copy()

    print(f"""Choose columns to fill by writing their numbers: '0, 2, 5, 12' """)
    na_columns = df.columns[df.isna().any()].tolist()
    for i, column in enumerate(na_columns, start=1):
        print(f"{i}. {column}")
    columns_input = input("""Which columns to fill:
    """)

    columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
    columns_to_fill = [na_columns[i] for i in columns_indexes]

    for column in columns_to_fill:

        if df[column].dtype == 'int64' or df[column].dtype == 'float':
            df = fill_na_values_numeric_column(dataframe=df, column_name=column)

        elif df[column].dtype == 'object' or df[column].dtype == 'boolean' or df[column].dtype == 'string' or pd.api.types.is_datetime64_any_dtype(df[column]):
            df = fill_na_values_categorical_column(dataframe=df, column_name=column)

        else:
            print(f"Data type of column '{column}' is not supported for filling")
    return df


def remove_missing_values(df):
    print(f"""Choose columns to remove missing values from by writing their numbers: '1, 2, 5, 12'""")
    data_type_columns = df.columns[df.isna().any()].tolist()
    for i, column in enumerate(data_type_columns, start=1):
        print(f"{i}. {column}: {df[column].isna().sum()} missing values")
    columns_input = input("""Which columns to correct:
    """)

    columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
    columns_to_correct = [data_type_columns[i] for i in columns_indexes]
    df_na_handled = df.dropna(subset=columns_to_correct)
    return df_na_handled


def handling_missing_values_in_df(df, remove_na):
    if remove_na == 'y':
        df_na_handled = remove_missing_values(df=df)
        remove_na_2 = input("""Do you now want to fill some missing values? (Enter 'y' to fill, 'n' to leave
""")
        if remove_na_2 == 'y':
            df_na_handled_2 = fill_missing_values(dataframe=df_na_handled)
        elif remove_na_2 == 'n':
            df_na_handled_2 = df_na_handled
        else:
            print(f"Unknown value. Leaving NA check.")
            df_na_handled_2 = df_na_handled
    elif remove_na == 'f':
        df_na_handled = fill_missing_values(dataframe=df)
        remove_na_2 = input("""Do you now want to remove some missing values? (Enter 'y' to remove, 'n' to leave
        """)
        if remove_na_2 == 'y':
            df_na_handled_2 = remove_missing_values(dataframe=df_na_handled)
        elif remove_na_2 == 'n':
            df_na_handled_2 = df_na_handled
        else:
            print(f"Unknown value. Leaving NA check.")
            df_na_handled_2 = df_na_handled
    elif remove_na == 'n':
        df_na_handled = df
    else:
        print(f"Unknown value. Leaving NA check.")
        df_na_handled_2 = df

    return df_na_handled_2


def na_cleaning(df):

    na_values_by_column = df.isna().sum()
    na_values_sum = na_values_by_column.sum()
    percentage_of_na = (na_values_sum/len(df)) * 100

    if percentage_of_na == 0.0:
        print(f'No missing values')
        df_na_handled = df.copy()

    elif percentage_of_na <= 5.0:
        print("Missing values are taking less than 5% of the dataset.")
        remove_na = input("""Remove them? (Enter 'y' to remove, 'f' to fill, 'n' to leave) 
""")
        df_na_handled = handling_missing_values_in_df(df, remove_na=remove_na)

    elif percentage_of_na > 5.0:
        print("Missing values are taking more than 5% of the dataset.")
        remove_na = input("""Remove them? (Enter 'y' to remove, 'f' to fill, 'n' to leave) 
""")
        df_na_handled = handling_missing_values_in_df(df, remove_na=remove_na)

    else:
        df_na_handled = df

    return df_na_handled


def data_na_cleaning_step(df):
    print("""Do you want to check for missing values?
'y' to check, 'n' to leave NA check""")
    na_check = input("")

    if na_check == 'y':
        df_na_handled = na_cleaning(df=df)
    elif na_check == 'n':
        df_na_handled = df.copy()
    else:
        print(f"Unknown value. Leaving NA check.")
        df_na_handled = df.copy()

    return df_na_handled