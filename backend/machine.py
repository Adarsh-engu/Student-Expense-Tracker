import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import calendar

def generate_spending_forecast(expenses_raw):
    """
    Takes a list of sqlite3.Row objects and returns a 
    formatted forecast array for Recharts.
    """
    if not expenses_raw or len(expenses_raw) < 5:
        return []

    # 1. Prepare Data
    df = pd.DataFrame(expenses_raw, columns=['date', 'amount'])
    df['date'] = pd.to_datetime(df['date'])
    df['YearMonth'] = df['date'].dt.to_period('M')
    
    monthly_totals = df.groupby('YearMonth')['amount'].sum().reset_index()
    monthly_totals = monthly_totals.sort_values('YearMonth')

    if len(monthly_totals) < 2:
        return []

    # 2. Train Linear Regression Model
    X = np.arange(len(monthly_totals)).reshape(-1, 1)
    y = monthly_totals['amount'].values
    model = LinearRegression()
    model.fit(X, y)

    # 3. Predict (Past + 2 Months Future)
    future_months = 2
    X_all = np.arange(len(monthly_totals) + future_months).reshape(-1, 1)
    predictions = model.predict(X_all)

    # 4. Format for Frontend
    forecast_data = []
    # Add Historical + AI Best Fit
    for i, row in monthly_totals.iterrows():
        period = row['YearMonth']
        forecast_data.append({
            "month": f"{calendar.month_abbr[period.month]} '{str(period.year)[-2:]}",
            "actual": round(float(row['amount']), 2),
            "predicted": round(float(predictions[i]), 2)
        })

    # Add Future Predictions
    last_period = monthly_totals.iloc[-1]['YearMonth']
    for i in range(1, future_months + 1):
        future_period = last_period + i
        forecast_data.append({
            "month": f"{calendar.month_abbr[future_period.month]} '{str(future_period.year)[-2:]}",
            "actual": None, 
            "predicted": round(float(predictions[len(monthly_totals) - 1 + i]), 2)
        })

    return forecast_data