import pandas as pd


def set_column_types_manually(df, subset):
    df_with_types = df
    for column in subset:
        print(f"Column: '{column}'. Random sample:")
        print((df_with_types[column]).sample(3).to_string(index=False))
        print(f"Which type to convert column '{column}' into? Current type: {(df[column]).dtype}")
        print("'f' for float, 'c' for categorical, 's' for string, 'd' for date, 'l' to leave")
        set_type = input("")
        if set_type == 'f':
            df_with_types = df_with_types.astype({column: 'float'})
        elif set_type == 'c':
            df_with_types = df_with_types.astype({column: 'object'})
        elif set_type == 's':
            df_with_types = df_with_types.astype({column: 'string'})
        elif set_type == 'd':
            df_with_types[column] = pd.to_datetime(df_with_types[column])
        elif set_type == 'l':
            pass
        else:
            print(f"Unknown type. Leaving default type '{(df_with_types[column]).dtype}' for column '{column}'")
            df_with_types = df_with_types
    return df_with_types


def setting_data_types_step(df):

    df_with_types = df

    print("""Want to set column data types manually?
'y' to set, 'n' to leave""")
    column_types = input("")
    print("")
    if column_types == 'y':

        print(f"""Choose columns to correct by writing their numbers: '1, 2, 5, 12'""")
        data_type_columns = df_with_types.columns.tolist()
        for i, column in enumerate(data_type_columns, start=1):
            print(f"{i}. {column}: {df_with_types[column].dtype}")
        columns_input = input("""Which columns to correct:
""")

        columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
        columns_to_correct = [data_type_columns[i] for i in columns_indexes]

        df_with_types = set_column_types_manually(df=df, subset=columns_to_correct)

        print("")
    elif column_types == 'n':
        df_with_types = df_with_types
    else:
        print(f"Unknown value. Leaving default data types.")
        df_with_types = df_with_types

    return df_with_types
