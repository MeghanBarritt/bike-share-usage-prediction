# Final Project - Bike Share Trends

## Project Task
I'm going to look at data from Washington DC covering the years 2011 and 2012, ((London Set)) to look for trends between time of day, time of year and weather conditions to try and predict bicycle rental rates.

## Process

### Datasets
Found the Washington DC Capital bike share data set on [the UC Irvine website](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) via a list of interesting datasets, and a second dataset on [Kaggle](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset) tracking the same variables when I checked for other data I could use. It was the only other dataset I found that had similar enough data to be usable in a short time frame. <br>

Confirmed the same basic data was available in both dataset. The London data required more processing to get to the same columns at the end, but aside from the DC set having an additional breakdown between regular and guest users, the data available was the same. 
<p>

</p>

### EDA
Explored data see distributions of various values, and to look for trends and possible correlations. Correlations with weather factors were more readily apparent to the human eye in the DC dataset, but there was significantly more usage overall in London.
<p>

</p>

### Feature Engineering
Performed feature engineering; all values related to time had to be extracted into columns for the London dataset. I also filled in gaps in the data where an hour had been skipped, using the assumption that those times had been omitted due to no bikes being rented, as for my purposes 'no rentals occured' is a useful data point. In the London set, there were some days that had no values at all, in any of the columns, which meant there was no way to fill most of them, so those entire days were dropped to avoid creating skew. Otherwise, different fill methods were used depending on the column; some columns have static values throughout the day, while others move coninuously. In the first case, the value from elsewhere in the day was simply placed, while in the second case interpolation was used to find the average between the values on either side of the missing value. <br>

For the DC dataset, a secondary table counting by day rather than by hour exists, so the weather values for a given day on that were used to fill missing weather values. No such second table existed for the London dataset, but exploration showed that it was reasonably common for the weather code on either side of a missing value to be the same, so simple forward fill was used to fill the missing values. <br>

The London dataset had different values in the `season`, `weather`, and `weekday` categories, so those were remapped to match the DC values. I am running them through separate models, but for consistency and so I don't confuse myself later, it made sense to have them match. In the case of the London weather encoding, it was significantly more granular than the DC encoding, so it **had** to be reformatted to be properly comparable. Both datasets have descriptions of what qualifies for each code, so I used those to group the London codes and match them to the DC ones. I also created a new `precip` column, based on those descriptions, which is a categorical 'is there precipitation or not' 0/1 column.<p>
_(Note: filling in the missing weather values in the London dataset happened after remapping the weather codes, and as the new values were less complex than the old ones, this may have helped with the values before and after the missing info being the same.)_<br>

The `temp`, `atemp` (apparent temp), `humidity` and `windspeed` columns of the DC dataset came pre-normalized, so the corresponding columns in the London dataset were normalized as well, using the MinMaxScaler, as that matched the behavior of the data as I found it. This was done before splitting to be consistent with the DC set. <br>
<p>

</p>

### Basic Models

I chose four regression models to try; `LinearRegression`, `SVR` and `RandomForestRegressor` from Sklearn, and the `XGBRegressor` from XGBoost. 

Because my datasets are time-based, I did my train/test split without shuffling.
<p>

</p>

#### **Linear Regression**<br>

>**_DC dataset_**<br>
>>_Train set_:<br>
>>Root Mean Squared Error: 129.47650158667653<br>
>>R-squared: 0.40023509636432963<br>
>---
>>_Test set_:<br>
>>Root Mean Squared Error: 182.47521094734591<br>
>>R-squared: 0.3154146362592527<br>


>_**London dataset**_<br>
>>_Train set_:<br>
>>Root Mean Squared Error: 887.6725962693262<br>
>>R-squared: 0.31692830959135165<br>
>---
>>_Test set_:<br>
>>Root Mean Squared Error: 978.3105148178599<br>
>>R-squared: 0.24876167392851933<br>

#### **SVR**<br>

>**_DC dataset_** <br>
>>_Train set_:<br>
>>Root Mean Squared Error: 143.88640899563978<br>
>>R-squared: 0.25930624378822176<br>
>---
>>_Test set_:<br>
>>Root Mean Squared Error: 210.58087348202932<br>
>>R-squared: 0.08828792531790608<br>


>**_London dataset_**  <br>
>>_Train set_:<br>
>>Root Mean Squared Error: 1021.256075397555<br>
>>R-squared: 0.09587189980290356<br>
>---<br>
>>_Test set_:<br>
>>Root Mean Squared Error: 1086.1229944892814<br>
>>R-squared: 0.07406114159332133<br>


#### **Random Forest Regressor**<br>

>**_DC dataset_** <br>
>>_Train set_:<br>
>>Root Mean Squared Error: 14.152513563206748<br>
>>R-squared: 0.9928341733910035<br>
>---<br>
>>_Test set_:<br>
>>Root Mean Squared Error: 72.87654665983804<br>
>>R-squared: 0.8908068409097215<br>


>_**London dataset**_ <br>
>>_Train set_:<br>
>>Root Mean Squared Error: 85.32546889684085<br>
>>R-squared: 0.9936887115704169<br>
>---<br>
>>_Test set_:<br>
>>Root Mean Squared Error: 289.163573168845<br>
>>R-squared: 0.9343686316506019<br>


#### **XGBRegressor**<br>

>**_DC dataset_** <br>
>>_Train set_:<br>
>>Root Mean Squared Error: 24.081214852442457<br>
>>R-squared: 0.9792529940605164<br>
>---<br>
>>_Test set_:<br>
>>Root Mean Squared Error: 69.92294989890084<br>
>>R-squared: 0.8994784355163574<br>


>**_London dataset_**<br>
>>_Train set_:<br>
>>Root Mean Squared Error: 127.9868120875735<br>
>>R-squared: 0.9857999086380005<br>
>>---<br>
>>_Test set_:
>>Root Mean Squared Error: 332.20786503370334<br>
>>R-squared: 0.9133748412132263<br>

<p>

The two models that performed the best, based on both `R-squared` and `root mean squarred error`, were the `RandomForest` and `XGBoost` models, so I chose those two models to continue tuning in the *hyperparameters* section.
<br>
</p>

### Feature Selection
I used three methods of feature selection. The first was running a simple `Lasso` regression, and retrieving all of the columns that did not return a coefficient of 0. This was the crudest of the methods, as the Lasso regression was completely untuned, and as a result removed the most features.<br>

The second method was `Forward Selection`, where features are added, step by step, to the model, starting with the most significant. <br>

My third mthod was `Backward Selection`; starting with all features and optimizing by attempting step by step removal of features. <br>

For both datasets, using Lasso selection resulted in the removal of multiple features. Forward and backwards select, however, dropped one feature from each set, and both dropped the same feature. Below are the selected and dropped features for each dataset, according to each method. <br>

_(Note: the `count` column is not involved here, as it is the dependant variable.)_

>_**Using Lasso**_:<br>
>_DC dataset_<br>
>>Selected features: season, year, month, day, hour, weekday, precip, temp, humidity<br>
>>Dropped features: holiday, workingday, weather, atemp, windspeed<br>
>---
>_London dataset_<br>
>>Selected features: season, year, month, day, hour, weekday, workingday, weather, precip, temp, humidity, windspeed<br>
>>Dropped features: holiday, atemp<br>


>_**Using Forward Select**_:<br>
>_DC dataset_<br>
>>Selected features: season, year, month, hour, weekday, holiday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: day, workingday<br>
>---
>_London dataset_<br>
>>Selected features: season, month, day, hour, workingday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: year, weekday, holiday<br>


>_**Using Backward Select**_:<br>
>_DC dataset_<br>
>>Selected features: season, year, month, hour, weekday, holiday, weather, precip, atemp, humidity, windspeed<br>
>>Dropped features: day, workingday, temp<br>
>---
>_London dataset_<br>
>>Selected features: season, month, day, hour, workingday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: year, weekday, holiday<br>

### Hyperparameter Tuning



### Pipelines




