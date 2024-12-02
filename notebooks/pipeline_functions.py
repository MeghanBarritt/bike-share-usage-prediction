import pandas as pd


def fill_hours_dc(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  
    
    all_hours = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    all_hours = pd.DataFrame({
        'date': all_hours.repeat(24), 
        'hour': list(range(24)) * len(all_hours)})
    all_hours['date'] = pd.to_datetime(all_hours['date'], errors='coerce')

    df_full = pd.merge(all_hours, df, on=['date', 'hour'], how='left')
    missing_rows = df_full[df_full.isnull().any(axis=1)]
    df_filled = pd.concat([df, missing_rows]).drop_duplicates().sort_values(by=['date', 'hour']).reset_index(drop=True)
    
    df_filled['count'] = df_filled['count'].fillna(0)

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
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    all_hours = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='h')
    all_hours = pd.DataFrame({'date': all_hours})
    all_hours['hour'] = all_hours['date'].dt.hour
    
    df_full = pd.merge(all_hours, df, on=['date', 'hour'], how='left')
    missing_rows = df_full[df_full.isnull().any(axis=1)]
    df_filled = pd.concat([df, missing_rows]).drop_duplicates().sort_values(by=['date', 'hour']).reset_index(drop=True)
    
    df_filled['count'] = df_filled['count'].fillna(0)

    return df_filled

