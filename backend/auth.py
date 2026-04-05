from flask import Blueprint, request, jsonify
from utils import get_db_connection 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)',
                     (data.get('full_name'), data.get('username'), data.get('password')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Registered successfully!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": "Username already exists or registration failed"}), 400

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                        (data.get('username'), data.get('password'))).fetchone()
    conn.close()

    if user:
        # THE FIX: Properly nesting the user data so React can read it
        return jsonify({
            "status": "success", 
            "message": "Welcome back!",
            "user": {
                "id": user['id'],
                "full_name": user['full_name'],
                "username": user['username']
            }
        }), 200
        
    return jsonify({"status": "error", "message": "Invalid username or password"}), 401