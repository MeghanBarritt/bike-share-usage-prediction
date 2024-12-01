# Final Project - Bike Share Trends

## Project Task
I'm going to look at data from Washington DC covering the years 2011 and 2012 ((London Set)) to look for trends between time of day, time of year and weather conditions to try and predict bicycle rental rates.

## Process

### Datasets
Found the Washington DC Capital bike share data set on [the UC Irvine website](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) via a list of interesting datasets, and a second dataset on [Kaggle](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset) tracking the same variables when I checked for other data I could use. It was the only other dataset I found that had similar enough data to be usable in a short time frame. 

Confirmed the same basic data was available in both dataset. The London data required more processing to get to the same columns at the end, but aside from the DC set having an additional breakdown between regular and guest users, the data available was the same. 

### EDA
Explored data see distributions of various values, and to look for trends and possible correlations. Correlations with weather factors were more readily apparent to the human eye in the DC dataset, but there was significantly more usage overall in London.

### Feature Engineering
Performed feature engineering; all values related to time had to be extracted into columns for the London dataset. I also filled in gaps in the data where an hour had been skipped, using the assumption that those times had been omitted due to no bikes being rented, as for my purposes 'no rentals occured' is a useful data point. In the London set, there were some days that had no values at all, in any of the columns, which meant there was no way to fill most of them, so those entire days were dropped to avoid creating skew. Otherwise, different fill methods were used depending on the column; some columns have static values throughout the day, while others move coninuously. In the first case, the value from elsewhere in the day was simply placed, while in the second case interpolation was used to find the average between the values on either side of the missing value. 

For the DC dataset, a secondary table counting by day rather than by hour exists, so the weather values for a given day on that were used to fill missing weather values. No such second table existed for the London dataset, but exploration showed that it was reasonably common for the weather code on either side of a missing value to be the same, so simple forward fill was used to fill the missing values. 

The London dataset had different values in the `season`, `weather`, and `weekday` categories, so those were remapped to match the DC values. I am running them through separate models, but for consistency and so I don't confuse myself later, it made sense to have them match. In the case of the London weather encoding, it was significantly more granular than the DC encoding, so it **had** to be reformatted to be properly comparable. Both datasets have descriptions of what qualifies for each code, so I used those to group the London codes and match them to the DC ones. I also created a new `precip` column, based on those descriptions, which is a categorical 'is there precipitation or not' 0/1 column.
_(Note: filling in the missing weather values in the London dataset happened after remapping the weather codes, and as the new values were less complex than the old ones, this may have helped with the values before and after the missing info being the same.)_

The `temp`, `atemp` (apparent temp), `humidity` and `windspeed` columns of the DC dataset came pre-normalized, so the corresponding columns in the London dataset were normalized as well, using the MinMaxScaler, as that matched the behavior of the data as I found it. This was done before splitting to be consistent with the DC set. 

### Basic Models
