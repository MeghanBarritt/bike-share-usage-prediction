import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class RenameColDC(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.name_map = {'dteday':'date','yr':'year','mnth':'month','hr':'hour',
        'weathersit':'weather','hum':'humidity','cnt':'count'}
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.rename(columns=self.name_map)
        
        return X
    

class FillHoursDC(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Make sure X is a DataFrame
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        df = X.copy()
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


class FillWMeans(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if 'season' in X.columns and 'date' in X.columns:
            X.loc[:,'season'] = X.groupby('date')['season'].transform(
                lambda x: x.fillna(x.mean()))
            
        if 'year' in X.columns and 'date' in X.columns:
            X.loc[:,'year'] = X.groupby('date')['year'].transform(
                lambda x: x.fillna(x.mean()))
            
        if 'month' in X.columns and 'date' in X.columns:
            X.loc[:,'month'] = X.groupby('date')['month'].transform(
                lambda x: x.fillna(x.mean()))
            
        if 'holiday' in X.columns and 'date' in X.columns:
            X.loc[:,'holiday'] = X.groupby('date')['holiday'].transform(
                lambda x: x.fillna(x.mean()))
            
        if 'weekday' in X.columns and 'date' in X.columns:
            X.loc[:,'weekday'] = X.groupby('date')['weekday'].transform(
                lambda x: x.fillna(x.mean()))
            
        if 'workingday' in X.columns and 'date' in X.columns:
            X.loc[:,'workingday'] = X.groupby('date')['workingday'].transform(
                lambda x: x.fillna(x.mean()))
            
        return X


class FillWInterpolate(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X.loc[:,'temp'] = X['temp'].interpolate(method='linear', limit_direction='both').round(2)
        X.loc[:,'atemp'] = X['atemp'].interpolate(method='linear', limit_direction='both').round(4)
        X.loc[:,'humidity'] = X['humidity'].interpolate(method='linear', limit_direction='both').round(2)
        X.loc[:,'windspeed'] = X['windspeed'].interpolate(method='linear', limit_direction='both').round(4)

        return X


class DateTimeConverter(BaseEstimator, TransformerMixin):
    def __init__(self, column_name):
        self.column_name = column_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Convert the specified column to datetime
        X[self.column_name] = pd.to_datetime(X[self.column_name], errors='coerce')
        return X


class MergeDataDC(BaseEstimator, TransformerMixin):
    def __init__(self, merge_df, on_column='date', how='left'):
        self.merge_df = merge_df
        self.merge_df.rename(columns={'dteday': 'date', 'weathersit': 'weather'}, inplace=True)
        self.on_column = on_column
        self.how = how

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Convert the 'dteday' column in both DataFrames to datetime if not already
        X[self.on_column] = pd.to_datetime(X[self.on_column], errors='coerce')
        self.merge_df[self.on_column] = pd.to_datetime(self.merge_df[self.on_column], errors='coerce')
        
        # Perform the merge
        X = X.merge(self.merge_df[[self.on_column, 'weather']], on=self.on_column, how=self.how)
        return X


class FillWeatherValueDC(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['weather_x'] = X['weather_x'].fillna(X['weather_y'])
        return X


class PrecipMappingDC(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.precip_map = {1: 0, 2: 0, 3: 1, 4: 1}
        self.name_map = {'weather_x': 'weather'}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['precip'] = X['weather_x'].map(self.precip_map)
        X = X.rename(columns=self.name_map)
        return X
    

class GetDay(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['day'] = X['date'].apply(lambda x: x.day)
        return X


class SetIntReorder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.col_list = ['season','year','month','holiday','weekday','workingday','weather','count']
        self.col_order = ['date','season','year','month','day','hour','weekday','holiday',
            'workingday','weather','precip','temp','atemp','humidity','windspeed','count']
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X[self.col_list] = X[self.col_list].astype(int)
        X = X[self.col_order]

        return X


class SetIndexDate(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.set_index('date')
        return X


class RenameColLond(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.name_map = {'cnt':'count','t1':'temp','t2':'atemp','hum':'humidity',
        'wind_speed':'windspeed','weather_code':'weather','is_holiday':'holiday',
        'timestamp':'date'}

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.rename(columns=self.name_map)
        
        return X
    

class MakeWorkingDayLond(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['workingday'] = 1
        
        # Assign 0 in appropriate rows based on holiday or weekend conditions
        X.loc[((X['holiday'] == 1.0) | (X['is_weekend'] == 1.0)), 'workingday'] = 0
        
        return X


class GetHour(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['hour'] = X['date'].apply(lambda x: x.hour)
        return X


class FillHoursLond(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()

        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        all_hours = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='h')
        all_hours = pd.DataFrame({'date': all_hours})
        all_hours['hour'] = all_hours['date'].dt.hour

        df_full = pd.merge(all_hours, df, on=['date', 'hour'], how='left')
        missing_rows = df_full[df_full.isnull().any(axis=1)]
        df_filled = pd.concat([df, missing_rows]).drop_duplicates().sort_values(by=['date', 'hour']).reset_index(drop=True)

        df_filled['count'] = df_filled['count'].fillna(0)

        return df_filled


class GetYr_Mn_Wkdy(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['year'] = X['date'].apply(lambda x: x.year)
        X['month'] = X['date'].apply(lambda x: x.month)
        X['weekday'] = X['date'].apply(lambda x: x.weekday())

        return X


class DropNaSubsetLond(BaseEstimator, TransformerMixin):
    def __init__(self, subset):
        self.subset = subset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.dropna(subset=self.subset)
        return X_transformed


class ForwardFillWeatherLond(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self
        
        def transform(self, X):
            X.loc[:, 'weather'] = X['weather'].ffill()
            return X


class ValueMapTransformerLond(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.seas_map= {0:1,1:2,2:3,3:4}
        self.weather_map = {1:1,2:1,3:2,4:2,7:3,10:4,26:4,94:4}
        self.day_map = {6:0,0:1,1:2,2:3,3:4,4:5,5:6}
        self.year_map = {2015:0,2016:1,2017:2}
        self.precip_map = {1:0,2:0,3:1,4:1}
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['season'] = X['season'].map(self.seas_map)
        X['weather'] = X['weather'].map(self.weather_map)
        X.loc[:,'weekday'] = X['weekday'].map(self.day_map)
        X.loc[:,'year'] = X['year'].map(self.year_map)
        X['precip'] = X['weather'].map(self.precip_map)

        return X