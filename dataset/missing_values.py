import pandas as pd


def numeric_fill_methods(df, column_name, fill, fill_limit=None):
    if fill == 'mean':
        df[column_name] = df[column_name].fillna(df[column_name].mean(), limit=fill_limit)
    elif fill == 'median':
        df[column_name] = df[column_name].fillna(df[column_name].median(), limit=fill_limit)
    else:
        pass
    return df


def categorical_fill_methods(df, column_name, fill, fill_limit=None):
    if fill == 'mode':
        df[column_name] = df[column_name].fillna(df[column_name].mode()[0], limit=fill_limit)
    elif fill == 'forward':
        df[column_name] = df[column_name].fillna(method='ffill', limit=fill_limit)
    elif fill == 'backward':
        df[column_name] = df[column_name].fillna(method='bfill', limit=fill_limit)
    else:
        df[column_name] = df[column_name].fillna(fill, limit=fill_limit)
    return df


def fill_na_values_numeric_column(df, column_name):
    column = column_name
    fill = input(f"""For column '{column}' (type integer/float) choose the replacement type: 'mean', 'median', 'mode', 'forward', 'backward'.
    Format:                                                'mean'
    Or enter custom value:                                 '0'
    Set limit to replace only first n missing values:      'median; limit = 3'
    Enter 'skip' to leave the column values as they are:   'skip'
    """)
    if fill == 'skip':
        pass
    else:
        fill_type = (fill.split(";", 1)[0])
        fill_limit = int(fill.split(";", 1)[1].replace(" ", "").replace("limit=", ""))
        fill_content = str(fill_type).strip()
        df[column] = numeric_fill_methods(df=df, column_name=column, fill=fill_content, fill_limit=fill_limit)
        df[column] = categorical_fill_methods(df=df, column_name=column, fill=fill_content, fill_limit=fill_limit)
    print(" ")
    return df


def fill_na_values_categorical_column(df, column_name):
    column = column_name
    fill = input(f"""For column '{column}' (type object, boolean, string or date) choose the replacement type: 'mode', 'forward', 'backward'.
    Format:                                                'mode'
    Or enter custom value:                                 '0'
    Set limit to replace only first n missing values:      'forward; limit = 3'
    Enter 'skip' to leave the column values as they are:   'skip'
    """)
    if fill == 'skip':
        pass
    else:
        fill_type = (fill.split(";", 1)[0])
        fill_limit = int(fill.split(";", 1)[1].replace(" ", "").replace("limit=", ""))
        fill_content = str(fill_type).strip()
        df[column] = categorical_fill_methods(df=df, column_name=column, fill=fill_content, fill_limit=fill_limit)
    print(" ")
    return df


def fill_missing_values(df):

    print(f"""Choose columns to fill by writing their numbers: '1, 2, 5, 12' """)
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


def handling_missing_values_in_df(df, handle_option):
    if handle_option == 'y':
        print("Filling missing values...")
        df_na_handled = fill_missing_values(df)

        print("Do you now want to remove some of the left missing values? (Enter 'y' for yes, 'n' for no)")
        remove_option = input()

        if remove_option == 'y':
            print("Removing remaining missing values...")
            df_na_handled_2 = remove_missing_values(df_na_handled)
        elif remove_option == 'n':
            df_na_handled_2 = df_na_handled
        else:
            print(f"Unknown value. Skipping removing missing values.")
            df_na_handled_2 = df_na_handled
    elif handle_option == 'n':
        df_na_handled_2 = df
    else:
        print(f"Unknown value. Skipping handling missing values")
        df_na_handled_2 = df

    return df_na_handled_2


def na_cleaning(df):

    na_values_by_column = df.isna().sum()
    na_values_sum = na_values_by_column.sum()
    percentage_of_na = (na_values_sum/len(df)) * 100

    if percentage_of_na == 0.0:
        print(f'No missing values')
        df_na_handled = df.copy()

    else:
        print(f"Missing values are taking {round(percentage_of_na, 2)}% of the dataset.")
        print("Choosing to handle missing values will first take you through the filling process and then the removal process.")
        remove_na = input("""Handle them? (Enter 'y' to handle, 'n' to leave) 
""")
        df_na_handled = handling_missing_values_in_df(df, handle_option=remove_na)

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
