# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 20:20:21 2025

@author: paulm
"""
import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

# Load the data (if not already loaded)
file_path = "C:/Users/paulm/OneDrive/Documents/MXN_VAR.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Preprocess the data
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df_clean = df.dropna()

# Rename columns for easier handling
df_clean.columns = [
    'spot_rate', 'us_10yr', 'mxn_10yr', 'tariff_rate',
    'us_cpi', 'us_gdp', 'us_unemployment',
    'us_industrial_prod', 'us_trade_balance'
]

# --- REDUCED VAR MODEL (5 variables) ---
selected_vars = ['spot_rate', 'us_10yr', 'mxn_10yr', 'us_gdp', 'us_cpi']
df_reduced = df_clean[selected_vars]

# Fit VAR model with maxlags=3
model_reduced = VAR(df_reduced)
results_reduced_fixed = model_reduced.fit(maxlags=3)

# Forecast next 4 quarters
forecast_reduced_fixed = results_reduced_fixed.forecast(df_reduced.values[-3:], steps=4)
forecast_df_reduced_fixed = pd.DataFrame(forecast_reduced_fixed, columns=selected_vars)
forecast_df_reduced_fixed.index = pd.date_range(start=df_reduced.index[-1] + pd.DateOffset(months=3), periods=4, freq='Q')

# Forecasted spot rate (baseline)
forecast_spot_rate_reduced_fixed = forecast_df_reduced_fixed[['spot_rate']]

# --- VAR MODEL WITH TARIFF SHOCK ---
selected_vars_with_tariff = ['spot_rate', 'us_10yr', 'mxn_10yr', 'us_gdp', 'us_cpi', 'tariff_rate']
df_with_tariff = df_clean[selected_vars_with_tariff]

# Fit VAR model with tariff
model_with_tariff = VAR(df_with_tariff)
results_with_tariff = model_with_tariff.fit(maxlags=3)

# Simulate sustained 25% tariff for 4 future quarters
last_known_with_tariff = df_with_tariff.iloc[-3:].copy()
future_with_tariff = pd.DataFrame(index=pd.date_range(start=df_with_tariff.index[-1] + pd.DateOffset(months=3), periods=4, freq='Q'))

for col in selected_vars_with_tariff:
    future_with_tariff[col] = last_known_with_tariff[col].iloc[-1]
future_with_tariff['tariff_rate'] = 0.25  # Apply tariff shock

# Forecast with shock model
forecast_with_tariff = results_with_tariff.forecast(df_with_tariff.values[-3:], steps=4)
forecast_with_tariff_df = pd.DataFrame(forecast_with_tariff, columns=selected_vars_with_tariff)
forecast_with_tariff_df.index = future_with_tariff.index

# Forecasted spot rate with 25% tariff
forecast_spot_rate_with_tariff = forecast_with_tariff_df[['spot_rate']]

# --- FINAL PLOT ---
plt.figure(figsize=(10, 6))

# Historical spot rate
df_with_tariff['spot_rate'].plot(label='Historical Spot Rate', linewidth=2, color='gray')

forecast_spot_rate_with_tariff.plot(label='Forecasted Spot Rate (25% Tariff)', linestyle='--', marker='o')

plt.title('USD/MXN Spot Rate Forecast with 25% Tariff Shock')
plt.xlabel('Date')
plt.ylabel('Spot Rate')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()