def duplicates_step(df):
    print("""Want to check for duplicates in data?
'y' to set, 'n' to leave""")
    duplicates_correction = input("")
    print("")
    if duplicates_correction == 'y':

        print(f"""Choose a subset of columns to check duplicates for by writing their numbers: '1, 2, 5, 12'""")
        duplicates_columns = df.columns.tolist()
        for i, column in enumerate(duplicates_columns, start=1):
            print(f"{i}. {column}: {df[column].dtype}")
        columns_input = input("""Which column subset to check:
""")

        columns_indexes = [int(index) - 1 for index in columns_input.split(",")]
        columns_to_correct = [duplicates_columns[i] for i in columns_indexes]

        duplicates = df[columns_to_correct].duplicated(keep='first')
        if duplicates.sum() > 0:
            print(f"Do you want to drop {duplicates.sum()} duplicates from the dataset? 'y' to drop, 'n' to leave")
            drop = input("")

            if drop == 'y':
                df_duplicates_cleaned = df.drop_duplicates(subset=columns_to_correct)
            elif drop == 'n':
                df_duplicates_cleaned = df
            else:
                df_duplicates_cleaned = df
        else:
            print("No duplicates found")
            df_duplicates_cleaned = df

        print("")
    elif duplicates_correction == 'n':
        df_duplicates_cleaned = df
    else:
        print(f"Unknown value. Leaving duplicates correction.")
        df_duplicates_cleaned = df

    return df_duplicates_cleaned
