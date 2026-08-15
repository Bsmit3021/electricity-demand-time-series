# Forecasting Electricity Demand in Georgia Using Machine Learning

This project compares six forecasting models, a naive forecast, linear
regression, SARIMA, Prophet, XGBoost, and LightGBM, to predict hourly
electricity demand one hour ahead for the Southern Company (SOCO)
balancing authority, which serves Georgia.

## What's in this repo

- `Electricity_Demand_Forecast_Analysis.ipynb`:
  the full analysis: data loading, cleaning, feature engineering, all six
  models, evaluation, and results.
- `data/`: the raw demand and weather data, plus the merged dataset the
  notebook builds from them. Already included, so you don't need to
  re-pull anything to run the analysis.
- `eia_to_csv.py` and `weather_pull.py`: the scripts originally used to
  pull the raw data. Only needed if you want to refresh the data or pull
  a different date range yourself; otherwise you can ignore these.

## How to run the analysis

1. **Install Python 3.9 or later** if you don't already have it.

2. **Install the required packages:**

   ```
   pip install pandas numpy matplotlib scikit-learn statsmodels prophet xgboost lightgbm
   ```

3. **Keep the folder structure as-is.** The notebook expects the CSV
   files to be in a `data/` folder sitting next to it.

4. **Open the notebook and run all cells in order**, top to bottom.

The full comparison table and all six models' results appear near the
end, under "Conclusion & Limitations."

## (Optional) Re-pulling the raw data

The `data/` folder already has everything you need, but if you want to
pull fresh data yourself:

```
python weather_pull.py
python eia_to_csv.py
```

Both scripts write directly into `data/`, matching the filenames the
analysis notebook expects.

## Notes

- Fitting SARIMA's hyperparameter grid takes a few minutes, that's the
  slowest part of the notebook; everything else runs quickly.
- If you get a package installation error, try adding `--user` to the
  pip install command above, or run it inside a virtual environment.

## Results summary

| Model | RMSE (MW) | MAE (MW) | MAPE (%) |
|---|---|---|---|
| Naive Forecast | 1,136.68 | 885.33 | 3.57 |
| Linear Regression | 860.19 | 626.41 | 2.54 |
| SARIMA(2,0,0)x(1,1,1,24) | 794.59 | 274.53 | 1.13 |
| Prophet (multi-step) | 2,530.39 | 1,944.09 | 7.53 |
| XGBoost | 524.12 | 252.47 | 0.98 |
| LightGBM | 507.34 | 236.63 | 0.93 |

LightGBM performed best overall. See the notebook's "Conclusion &
Limitations" section for the full discussion, including why Prophet's
results aren't directly comparable to the other five models.
