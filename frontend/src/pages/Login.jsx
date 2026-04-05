import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username,
        password
      });
      setMessage("✅ " + response.data.message);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (error) {
      if (error.response && error.response.data) {
        setMessage("❌ " + error.response.data.message);
      } else {
        setMessage("❌ Server error. Make sure Python is running!");
      }
    }
  };
  return (
    <div className="login-wrapper">
      <div className="main-container">
        <div className="image-section">
          <img
            src="https://cdn-icons-png.flaticon.com/512/2331/2331970.png"
            alt="Money Icon"
            className="brand-icon"
          />
          <h1>Student Expense Tracker</h1>
          <p>Powered by Machine Learning</p>
        </div>
        <div className="form-section">
          <form className="login-form" onSubmit={handleLogin}>
            <h2>System Login</h2>
            <div className="input-group">
              <input 
                id="username" 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required 
              />
              <label htmlFor="username">Username</label>
            </div>
            <div className="input-group">
              <input 
                id="password" 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required 
              />
              <label htmlFor="password">Password</label>
            </div>
            {/* Display error/success messages here */}
            {message && (
              <p style={{ 
                color: message.includes('✅') ? '#00ff9d' : '#ff4757', 
                textAlign: 'center', 
                marginBottom: '15px', 
                fontSize: '14px', 
                fontWeight: '600' 
              }}>
                {message}
              </p>
            )}
            <button type="submit" className="submit-btn">Login</button>

            <p className="bottom-text">
              New user? 
              <Link to="/register">Create Account</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}