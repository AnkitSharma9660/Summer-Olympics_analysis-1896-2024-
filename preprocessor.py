import pandas as pd



def preprocess(df,region_df):

    #merge df with region_df
    df = df.merge(region_df, on='NOC', how='left')

    #one hot encoding medal
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df