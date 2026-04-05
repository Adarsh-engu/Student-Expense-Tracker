from flask import Blueprint, request, jsonify
import pandas as pd
from utils import get_db_connection 

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/api/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (user_id, date, title, amount, category) VALUES (?, ?, ?, ?, ?)',
                     (data['user_id'], data['date'], data['title'], float(data['amount']), data['category']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Expense logged!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@expenses_bp.route('/api/upload-csv', methods=['POST'])
@expenses_bp.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    user_id = request.form.get('user_id')
    try:
        df = pd.read_csv(file)
        row_count = len(df) # <--- 🧠 Calculate the exact number of rows!
        
        conn = get_db_connection()
        for _, row in df.iterrows():
            conn.execute('INSERT INTO expenses (user_id, date, title, amount, category) VALUES (?, ?, ?, ?, ?)',
                         (user_id, str(row['Date']), row['Title'], float(row['Amount']), row['Category']))
        conn.commit()
        conn.close()
        
        # Send the dynamic message back to React
        return jsonify({"status": "success", "message": f"{row_count} rows of data were inserted!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@expenses_bp.route('/api/get-expenses/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    try:
        conn = get_db_connection()
        # FIX: Removed 'LIMIT 50' so the dashboard can see all 18 months of history!
        expenses = conn.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,)).fetchall()
        conn.close()
        return jsonify({"status": "success", "expenses": [dict(exp) for exp in expenses]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500