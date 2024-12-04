# Final Project - Bike Share Trends

## Project Task<br>
I looked at data from two cities, Washington DC and London England, over two year time spans, to try and find weather-related usage patterns in the cities' bikeshare systmes.<br>

from Washington DC covering the years 2011 and 2012, and from London, England. The London data also covers two years, but covers January 4, 2015 to January 3, 2017.  to look for trends between time of day, time of year and weather conditions to try and predict bicycle rental rates. <br>

## Process

### Datasets<br>

Found the Washington DC Capital bike share data set on [the UC Irvine website](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) via a list of interesting datasets, and a second dataset on [Kaggle](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset) tracking the same variables when I checked for other data I could use. It was the only other dataset I found that had similar enough data to be usable in a short time frame. <br>

Confirmed the same basic data was available in both dataset. The London data required more processing to get to the same columns at the end, but aside from the DC set having an additional breakdown between regular and guest users, the data available was the same. <br>

The DC data starts on January 1, 2011, and ran for two years, ending on December 31, 2012. The London data missed the New Year and instead starts on January 4, and also runs for two years, but from 2015 until January 3, 2017. <br>

Both datasets include hourly weather data; temperature, humidity, windspeed and 'weather condition', as well as whether or not a day is a holiday, the season, and of course the number of rentals. 
<p>
<br>
</p>

### EDA
Explored data see distributions of various values, and to look for trends and possible correlations. Correlations with weather factors were more readily apparent to the human eye in the DC dataset, but there was significantly more usage overall in London.
<p>
<br>
</p>

### Feature Engineering
Performed feature engineering; all values related to time had to be extracted into columns for the London dataset. I also filled in gaps in the data where an hour had been skipped, using the assumption that those times had been omitted due to no bikes being rented, as for my purposes 'no rentals occured' is a useful data point. In the London set, there were some days that had no values at all, in any of the columns, which meant there was no way to fill most of them, so those entire days were dropped to avoid creating skew. Otherwise, different fill methods were used depending on the column; some columns have static values throughout the day, while others move coninuously. In the first case, the value from elsewhere in the day was simply placed, while in the second case interpolation was used to find the average between the values on either side of the missing value. <br>

For the DC dataset, a secondary table counting by day rather than by hour exists, so the weather values for a given day on that were used to fill missing weather values. No such second table existed for the London dataset, but exploration showed that it was reasonably common for the weather code on either side of a missing value to be the same, so simple forward fill was used to fill the missing values. <br>

The London dataset had different values in the `season`, `weather`, and `weekday` categories, so those were remapped to match the DC values. I am running them through separate models, but for consistency and so I don't confuse myself later, it made sense to have them match. In the case of the London weather encoding, it was significantly more granular than the DC encoding, so it **had** to be reformatted to be properly comparable. Both datasets have descriptions of what qualifies for each code, so I used those to group the London codes and match them to the DC ones. I also created a new `precip` column, based on those descriptions, which is a categorical 'is there precipitation or not' 0/1 column.<p>
_(Note: filling in the missing weather values in the London dataset happened after remapping the weather codes, and as the new values were less complex than the old ones, this may have helped with the values before and after the missing info being the same.)_<br>

The `temp`, `atemp` (apparent temp), `humidity` and `windspeed` columns of the DC dataset came pre-normalized, so the corresponding columns in the London dataset were normalized as well, using the MinMaxScaler, as that matched the behavior of the data as I found it. This was done before splitting to be consistent with the DC set. <br>
<p>
<br>
</p>

### Basic Models

I chose four regression models to try; `LinearRegression`, `SVR` and `RandomForestRegressor` from Sklearn, and the `XGBRegressor` from XGBoost. 

Because my datasets are time-based, I did my train/test split without shuffling.
<p>

</p>


>Linear Regression<br>
>---
>**DC dataset**<br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 129.47650158667653<br>
>>R-squared: 0.40023509636432963<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 182.47521094734591<br>
>>R-squared: 0.3154146362592527<br>
>___
>___
>**London dataset**<br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 887.6725962693262<br>
>>R-squared: 0.31692830959135165<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 978.3105148178599<br>
>>R-squared: 0.24876167392851933<br>
>___
<p>
<br>

>SVR<br>
>---
>**DC dataset** <br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 143.88640899563978<br>
>>R-squared: 0.25930624378822176<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 210.58087348202932<br>
>>R-squared: 0.08828792531790608<br>
>___
>___
>**London dataset**  <br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 1021.256075397555<br>
>>R-squared: 0.09587189980290356<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 1086.1229944892814<br>
>>R-squared: 0.07406114159332133<br>
>___
<p>
<br>

>Random Forest Regressor<br>
>---
>**DC dataset** <br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 14.152513563206748<br>
>>R-squared: 0.9928341733910035<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 72.87654665983804<br>
>>R-squared: 0.8908068409097215<br>
>___
>___
>**London dataset** <br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 85.32546889684085<br>
>>R-squared: 0.9936887115704169<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 289.163573168845<br>
>>R-squared: 0.9343686316506019<br>
>___
<p>
<br>

>XGBRegressor<br>
>---
>**DC dataset** <br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 24.081214852442457<br>
>>R-squared: 0.9792529940605164<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 69.92294989890084<br>
>>R-squared: 0.8994784355163574<br>
>>___
>>___
>**London dataset**<br>
>___
>>_Train set_:<br>
>>Root Mean Squared Error: 127.9868120875735<br>
>>R-squared: 0.9857999086380005<br>
>>___
>>_Test set_:<br>
>>Root Mean Squared Error: 332.20786503370334<br>
>>R-squared: 0.9133748412132263<br>
>___

<p>

The two models that performed the best, based on both `R-squared` and `root mean squarred error`, were the `RandomForest` and `XGBoost` models, so I chose those two models to continue tuning in the *hyperparameters* section.
<br>
</p>
<p>
<br>
</p>

### Feature Selection <br>
I used three methods of feature selection. The first was running a simple `Lasso` regression, and retrieving all of the columns that did not return a coefficient of 0. This was the crudest of the methods, as the Lasso regression was completely untuned, and as a result removed the most features.<br>

The second method was `Forward Selection`, where features are added, step by step, to the model, starting with the most significant. <br>

My third mthod was `Backward Selection`; starting with all features and optimizing by attempting step by step removal of features. <br>

For both datasets, using Lasso selection resulted in the removal of multiple features. Forward and backwards select, however, dropped one feature from each set, and both dropped the same feature. Below are the selected and dropped features for each dataset, according to each method. <br>

_(Note: the `count` column is not involved here, as it is the dependant variable.)_

>**Using Lasso**:<br>
>___
>_DC dataset_<br>
>>Selected features: season, year, month, day, hour, weekday, precip, temp, humidity<br>
>>Dropped features: holiday, workingday, weather, atemp, windspeed<br>
>---
>_London dataset_<br>
>>Selected features: season, year, month, day, hour, weekday, workingday, weather, precip, temp, humidity, windspeed<br>
>>Dropped features: holiday, atemp<br>
>___
<p>
<br>

>**Using Forward Select**:<br>
>___
>_DC dataset_<br>
>>Selected features: season, year, month, hour, weekday, holiday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: day, workingday<br>
>---
>_London dataset_<br>
>>Selected features: season, month, day, hour, workingday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: year, weekday, holiday<br>
>___
<p>
<br>

>**Using Backward Select**:<br>
>___
>_DC dataset_<br>
>>Selected features: season, year, month, hour, weekday, holiday, weather, precip, atemp, humidity, windspeed<br>
>>Dropped features: day, workingday, temp<br>
>---
>_London dataset_<br>
>>Selected features: season, month, day, hour, workingday, weather, precip, temp, atemp, humidity, windspeed<br>
>>Dropped features: year, weekday, holiday<br>
>___

I created new versions of X_train and X_test based on each selection list, as I wanted to test how well the model could do with feature inputs that had, theoretically been optimized. <br>

Because forward and backwards select on the London dataset produced the same feature list, I didn't bother to create a separate `_fw` and `_bw` train/test pair; it would have been redundant. I simply created a `_fwbw` pair instead. <br>
<p>
</p>

### Hyperparameter Tuning
To start with, I tuned both models on the regular train/test set that had all of the features. My initial attempts to use `r2` as my scoring method produced very low scores, so I ran secondary versions scoring on `neg_root_mean_squared_error`, and found that while that method did not always produce improvement, it usually at least matched the untuned model's baseline.<br>

>Random Forest: <br>
>---
>>**DC set**: <br>
>>Base model r2: 0.8908068409097215 <br>
>>Tuned model r2: 0.6895321510957303<br>
>>___
>>Base model rmse: 72.87654665983804 <br>
>>Tuned model rmse: 71.84172119174976<br>
>___
>___
>>**London set**: <br>
>>Base model r2: 0.9343686316506019 <br>
>>Tuned model r2: 0.9028084805222928<br>
>>____
>>Base model rmse: 289.163573168845 <br>
>>Tuned model rmse: 312.8454875514148<br>
>___
<p>
<br>

>XGBoost: <br>
>---
>>**DC set**: <br>
>>Base model r2: 0.8994784355163574 <br>
>>Tuned model r2: 0.7963137030601501<br>
>>___
>>Base model rmse: 69.92294989890084 <br>
>>Tuned model rmse: 56.490411500995606<br>
>___
>___
>>**London set**: <br>
>>Base model r2: 0.9133748412132263 <br>
>>Tuned model r2: 0.919543719291687<br>
>>___
>>Base model rmse: 332.20786503370334 <br>
>>Tuned model rmse: 293.8955040541115<br>
>___
<p>
<br>
</p>

`XGBRegressor` performed much better than `RandomForestRegressor` did, so for the feature selection models, I focused on that one. <br>
<p>


>XGBR, Root Mean Squared Error <br>
>---
>>**DC set**: <br>
>>Base model: 69.92294989890084 <br>
>>All features: 56.490411500995606 <br>
>>Fw features: 56.5705918807984<br>
>>Bw features: 55.76142506506576 <br>
>>Lasso features: 60.833681953480436 <br>
>___
>___
>>**London set**: <br>
>>Base model: 332.20786503370334<br>
>>All features: 293.8955040541115 <br>
>>FwBw features: 287.72959089223957 <br>
>>Lasso features: 287.6278104393208<br>
>___
<p>
<br>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>alpha</th>
      <th>lambda</th>
      <th>learning_rate</th>
      <th>max_depth</th>
      <th>n_estimators</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>dc allfeat</th>
      <td>0.10</td>
      <td>100</td>
      <td>0.3</td>
      <td>6</td>
      <td>180</td>
    </tr>
    <tr>
      <th>dc_fw</th>
      <td>2.00</td>
      <td>50</td>
      <td>0.2</td>
      <td>6</td>
      <td>370</td>
    </tr>
    <tr>
      <th>dc_bw</th>
      <td>0.70</td>
      <td>80</td>
      <td>0.2</td>
      <td>6</td>
      <td>280</td>
    </tr>
    <tr>
      <th>dc_lasso</th>
      <td>1.00</td>
      <td>130</td>
      <td>0.2</td>
      <td>6</td>
      <td>190</td>
    </tr>
    <tr>
      <th>lond_allfeat</th>
      <td>0.75</td>
      <td>125</td>
      <td>0.3</td>
      <td>7</td>
      <td>70</td>
    </tr>
    <tr>
      <th>lond_fwbw</th>
      <td>0.01</td>
      <td>10</td>
      <td>0.1</td>
      <td>7</td>
      <td>140</td>
    </tr>
    <tr>
      <th>lond_lasso</th>
      <td>0.01</td>
      <td>10</td>
      <td>0.1</td>
      <td>6</td>
      <td>160</td>
    </tr>
  </tbody>
</table>
</div>
<p>
<br>
The DC set was all over the place for alpha and lambda values, and had the highest values for number of estimators, in one case going twice as high as the highest estimator value any London model ended up with. <br>

The London set had higher alpha and lambda values on the all features version, but it dropped down for versions that had undergone feature selection. The number of estimators did the opposite, jumping up where feature election had occured.<br>

Both models had the learning rate decrease for versions that had undergone feature selection, with a larger decrease on the London set. <br>

The DC dataset always used a max depth of 6, but the London dataset slightly prefered 7, with no apparent pattern. <br>

<p>
<br>
</p>

### Tuned Models

I initiated and ran each model tuned in the hyperparameters notebook so I could fully evaluate their performances.<br>

During my evaluation and comparisson, I compared the tuned models for each set to the untuned one, and the overall behavior of each dataset to the other. I looked at the `R-squared` and `Root Mean Squared Error` (R2 and RMSE) of both the training and test sets, as well as the changes between them, and the RMSE as a percentage of each dataset's maximum real value, in order to get an idea of how much error there actually was; an error of +/-50 would not be a big deal when the values in question are routinely in the thousands, but *would* be a big deal if the values were dozens at most. <br>
<p>

**DC evaluation outputs**

</p>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Train R2</th>
      <th>Test R2</th>
      <th>R2 Decrease</th>
      <th>Train RMSE</th>
      <th>Test RMSE</th>
      <th>RMSE as % of range</th>
      <th>RMSE Increase</th>
      <th>RMSE Increase as % of range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>basic model</th>
      <td>0.979</td>
      <td>0.899</td>
      <td>0.080</td>
      <td>24.081</td>
      <td>69.923</td>
      <td>7.16</td>
      <td>35.832</td>
      <td>3.67</td>
    </tr>
    <tr>
      <th>all features</th>
      <td>0.973</td>
      <td>0.903</td>
      <td>0.070</td>
      <td>27.238</td>
      <td>68.692</td>
      <td>7.03</td>
      <td>41.454</td>
      <td>4.24</td>
    </tr>
    <tr>
      <th>fw select</th>
      <td>0.975</td>
      <td>0.908</td>
      <td>0.066</td>
      <td>26.683</td>
      <td>66.804</td>
      <td>6.84</td>
      <td>40.120</td>
      <td>4.11</td>
    </tr>
    <tr>
      <th>bw select</th>
      <td>0.967</td>
      <td>0.898</td>
      <td>0.069</td>
      <td>30.417</td>
      <td>70.396</td>
      <td>7.21</td>
      <td>39.979</td>
      <td>4.09</td>
    </tr>
    <tr>
      <th>lasso</th>
      <td>0.954</td>
      <td>0.889</td>
      <td>0.065</td>
      <td>35.664</td>
      <td>73.389</td>
      <td>7.51</td>
      <td>37.725</td>
      <td>3.86</td>
    </tr>
  </tbody>
</table>
</div>
<p>
<br>
All the test R2 values are very consistent, regardless of model tuning or feature set, while the drop in R2 between the training and test sets is smaller for the tuned models, and even smaller with feature selection. <p>

The test RMSEs are all also very similar, both as actual values and as percentages of the maximum possible value. While the actual values of the error increases look quite large, approximately doubleing across the board, they are actually fairly small amounts in proportion to the overall range.<p>

There is not much difference in the `RMSE as %` values (0.67) *or* in the `RMSE Increase as %` values, even though there was some improvement in how much the R2 was dropping. This could mean the model is not generalizing very well on this data, even after tuning and feature selection. <p>

For this data, there wasn't a consistent pattern to the performance in the raw scores, only in the amount of change from the training to test sets. 
</p>
<br>

**London evaluation outputs**

</p>
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Train R2</th>
      <th>Test R2</th>
      <th>R2 Decrease</th>
      <th>Train RMSE</th>
      <th>Test RMSE</th>
      <th>RMSE as % of range</th>
      <th>RMSE Increase</th>
      <th>RMSE Increase as % of range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>basic model</th>
      <td>0.986</td>
      <td>0.913</td>
      <td>0.072</td>
      <td>127.987</td>
      <td>332.208</td>
      <td>4.23</td>
      <td>203.221</td>
      <td>2.59</td>
    </tr>
    <tr>
      <th>all features</th>
      <td>0.968</td>
      <td>0.929</td>
      <td>0.038</td>
      <td>193.013</td>
      <td>299.935</td>
      <td>3.82</td>
      <td>106.922</td>
      <td>1.36</td>
    </tr>
    <tr>
      <th>fwbw select</th>
      <td>0.964</td>
      <td>0.928</td>
      <td>0.036</td>
      <td>203.815</td>
      <td>302.494</td>
      <td>3.85</td>
      <td>98.679</td>
      <td>1.26</td>
    </tr>
    <tr>
      <th>lasso</th>
      <td>0.969</td>
      <td>0.936</td>
      <td>0.033</td>
      <td>189.722</td>
      <td>286.016</td>
      <td>3.64</td>
      <td>96.293</td>
      <td>1.23</td>
    </tr>
  </tbody>
</table>
</div>
<p>
<br>
The R2 values for the test set are, again, very consistent. This time, however, there is a much smaller drop between the training and the test, showing that the model is better at generalizing and is not overfitting. There is no difference between the version with all features included and the train/tests produced by feature selection. <p>

Here there is more variation in RMSE, with improvement in all of the tuned models, and looking at it as a percentage of the maximum possible value, it is easier to see the magnitude of the changes. The model with its features selected by `Lasso` had the largest decrease, 0.59, with the other two having around 0.4.<p>

The increase in error between training and test was not similar for this model. Tuning cut the increase down dramatically for all versions. The models with feature selection had less than half the untuned model's RMSE increase. The 'all features' version was only just above the 50% mark. So, even though the actual test RMSE values were fairly close together, most of that error wasn't a result of the transition from training to test, but part of the models' attempts to account for the data. This, combined with the high R2 scores, is a good sign for the models' abilities to account for the data without overfitting. 
</p>
Further confirmation that the models are doing well can be seen in comparing the error on the variable being predicted, `count`, to its standard deviation in the original data. For the DC dataset it is **181.5**, while the highest test RMSE is ~73. For London those numbers are 1085.4 and ~332, respectively. In both cases, the RMSE is less than 1/3 of the standard deviation; well within "reasonable" for the data.<p>
<br>
</p>

**Model Comparisons**<p>
I ranked the models for each set by looking at the `Test R2` and `R2 Decrease` columns, as well as the `Test RMSE` and `RMSE Increase` columns, ignoring the training columns as they are not the target, and the other two RMSE columns as they were redundant. I put values starting at 1 for the best and so on (up to 5 for DC and 4 for London) in each column, and then added the total for each model, with the lowest value being the best overall performer. <p>

|     DC     | Test R2 | R2 Decrease | Test RMSE| RMSE Increase | Total |
|------------|---------|-------------|----------|---------------|-------| 
|basic model |	3	   |      5      |	  3     |	   1        |	12  |
|all features|	2      |   	  4      |	  2     |	   5        |	13  |
|fw select   |	1      |   	  2      |	  1     |	   4        |	8   | 
|bw select   |	4      |      3      |	  4     |	   3        |	14  |
|lasso       |	5      |   	  1      |	  5     |	   2        |	13  |
|            |         |             |          |               |       |

Here, `Forward Select` had the best overall results, with all the others being pretty similar.<br>
<br>

|   London	 | Test R2 | R2 Decrease | Test RMSE| RMSE Increase | Total |
|------------|---------|-------------|----------|---------------|-------|
|basic model |	  4    |	  4      |     4    |	    4       |	16  |
|all features|	  2    |	  3      |	   2    |	    3       |	10  |
|fwbw select |	  3    |	  2      |	   3    |	    2       |	10  |
|lasso	     |    1    |	  1      |	   1    |	    1       |	 4  |  
|            |         |             |          |               |       |

Here, the basic model, with no tuning, always performed the worst, while the model using `Lasso` selected features always performed the best, albiet by very small margins.  


| Model            | Test R2 | R2 Decrease | RMSE % | RMSE Up % |
|------------------|---------|-------------|--------|-----------|
| DC Base          |    0.899|        0.080|    7.16|       3.67|
| London Base      |    0.913|        0.072|	4.23|	    2.59|
|                  |         |             |        |           |
| DC Tuned Avg     |    0.889|        0.068|    7.15|       4.08|
| London Tuned Avg |    0.931|        0.036|    3.77|       1.28|
|                  |         |             |        |           |

Despite having identical features to work with, the model does slightly better with the London dataset, especially after tuning. I am not sure if this is down to noise, or if there is a stronger pattern in the London set. Given that there is a more prevelant bike riding culture in Europe generally, this is the opposite of what I would have expected. 

<p>
<br>
</p>

### Pipelines




 


