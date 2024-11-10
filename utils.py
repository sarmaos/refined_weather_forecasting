import pandas as pd

def normalize_df(df, cols, normalize_col):
    values_df = pd.json_normalize(df[normalize_col])
    df = df.drop(columns=[normalize_col]).join(values_df)
    return df[cols]

def normalize_city_param(source):
    pass