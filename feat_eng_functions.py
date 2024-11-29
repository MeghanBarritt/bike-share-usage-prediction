import pandas as pd
from datetime import datetime 


def fill_hours_dc(df):
    df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')  
    
    all_hours = pd.date_range(start=df['dteday'].min(), end=df['dteday'].max(), freq='D')
    all_hours = pd.DataFrame({
        'dteday': all_hours.repeat(24), 
        'hr': list(range(24)) * len(all_hours)})
    all_hours['dteday'] = pd.to_datetime(all_hours['dteday'], errors='coerce')

    df_full = pd.merge(all_hours, df, on=['dteday', 'hr'], how='left')
    missing_rows = df_full[df_full.isnull().any(axis=1)]
    df_filled = pd.concat([df, missing_rows]).drop_duplicates().sort_values(by=['dteday', 'hr']).reset_index(drop=True)
    
    df_filled['cnt'] = df_filled['cnt'].fillna(0)

    return df_filled

def get_day(date):
    day_o_m = date.day
    return day_o_m

def get_hour(date):
    hour = date.hour
    return hour

def get_year(date):
    year = date.year
    return year

def get_month(date):
    month = date.month
    return month

def get_weekday(date):
    weekday = date.weekday()
    return weekday

def fill_hours_london(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    all_hours = pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='h')
    all_hours = pd.DataFrame({'timestamp': all_hours})
    all_hours['hour'] = all_hours['timestamp'].dt.hour
    
    df_full = pd.merge(all_hours, df, on=['timestamp', 'hour'], how='left')
    missing_rows = df_full[df_full.isnull().any(axis=1)]
    df_filled = pd.concat([df, missing_rows]).drop_duplicates().sort_values(by=['timestamp', 'hour']).reset_index(drop=True)
    
    df_filled['cnt'] = df_filled['cnt'].fillna(0)

    return df_filled

