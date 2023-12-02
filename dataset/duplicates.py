def duplicates_step(df):
    print("""Want to handle duplicates in data?
'y' to set, 'n' to leave""")
    duplicates_correction = input("")
    print("")
    if duplicates_correction == 'y':

        print(f"""Choose a subset of columns to drop duplicates for (leaves first occurance) by writing their numbers: '1, 2, 5, 12'""")
        duplicates_columns = df.columns.tolist()
        for i, column in enumerate(duplicates_columns, start=1):
            print(f"{i}. {column}: {df[column].dtype}")
        columns_input = input("""Which columns to correct:
""")

        columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
        columns_to_correct = [duplicates_columns[i] for i in columns_indexes]

        df_duplicates_cleaned = df.drop_duplicates(subset=columns_to_correct)

        print("")
    elif duplicates_correction == 'n':
        df_duplicates_cleaned = df
    else:
        print(f"Unknown value. Leaving default data types.")
        df_duplicates_cleaned = df

    return df_duplicates_cleaned
