# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 21:51:33 2025

@author: paulm
"""
import pandas as pd

# Load the Excel file to inspect its contents
excel_path = "C:/Users/paulm/OneDrive/Documents/VAR_work.xlsx"
xls = pd.ExcelFile(excel_path)
sheet_names = xls.sheet_names
sheet_names

# Load the data from the first sheet
df = xls.parse('Sheet1')
df.head()

from statsmodels.tsa.stattools import adfuller

# Prepare the data
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Run ADF test on each column
adf_results = {}
for column in df.columns:
    result = adfuller(df[column].dropna())
    adf_results[column] = {
        'ADF Statistic': result[0],
        'p-value': result[1],
        'Stationary': result[1] < 0.05
    }

adf_df = pd.DataFrame(adf_results).T
print(adf_df)


# Take first differences to make the series stationary
df_diff = df.diff().dropna()

# Run ADF test again on the differenced data
adf_diff_results = {}
for column in df_diff.columns:
    result = adfuller(df_diff[column].dropna())
    adf_diff_results[column] = {
        'ADF Statistic': result[0],
        'p-value': result[1],
        'Stationary': result[1] < 0.05
    }

adf_diff_df = pd.DataFrame(adf_diff_results).T
adf_diff_df

# Try with maxlags = 2
from statsmodels.tsa.api import VAR

# Select optimal lag order using AIC
model = VAR(df_diff)
lag_order_results = model.select_order(maxlags=2)
optimal_lag = lag_order_results.aic

# Fit the VAR model with the optimal lag length
fitted_model = model.fit(optimal_lag)

# Show a summary of the fitted model
model_summary = fitted_model.summary()
model_summary
