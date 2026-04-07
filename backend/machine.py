import pandas as pd
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

def train_and_predict(user_id):
    try:
        # 1. Load data from your SQLite DB
        conn = sqlite3.connect('expenses.db')
        query = f"SELECT date, amount FROM expenses WHERE user_id = {user_id}"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty or len(df) < 10:
            return 2500.0  # Fallback dummy value if not enough data

        # 2. Pre-process: Group by Month
        df['date'] = pd.to_datetime(df['date'])
        # Create a 'Month Index' (e.g., Month 1, Month 2...) for the model to understand
        df['month_year'] = df['date'].dt.to_period('M')
        monthly_summary = df.groupby('month_year')['amount'].sum().reset_index()
        
        # We need at least 2 months to draw a line!
        if len(monthly_summary) < 2:
            return round(float(monthly_summary['amount'].iloc[0]), 2)

        monthly_summary['month_index'] = np.arange(len(monthly_summary)).reshape(-1, 1)

        # 3. Train the Linear Regression Model
        X = monthly_summary[['month_index']] # Features (Time)
        y = monthly_summary['amount']        # Target (Spend)
        
        model = LinearRegression()
        model.fit(X, y)

        # 4. Predict for the NEXT month
        next_month = np.array([[len(monthly_summary)]])
        prediction = model.predict(next_month)

        return round(float(prediction[0]), 2)

    except Exception as e:
        print(f"🤖 ML Error: {e}")
        return 0.0