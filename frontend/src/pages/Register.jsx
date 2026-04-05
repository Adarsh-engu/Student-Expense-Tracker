import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Register.css';

export default function Register() {
  const [fullName, setFullName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [college, setCollege] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState(''); 
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage(''); 
    
    if (password !== confirmPassword) {
      setMessage("❌ Passwords do not match!");
      return;
    }
    
    try {
      // THE FIX: Mapping the payload keys exactly to what Python expects
      const response = await axios.post('http://127.0.0.1:5000/api/register', {
        full_name: fullName, 
        username: username,
        password: password
      });
      
      setMessage("✅ " + response.data.message);
      
      setTimeout(() => {
        navigate('/');
      }, 2000);
      
    } catch (error) {
      if (error.response && error.response.data) {
        setMessage("❌ " + error.response.data.message);
      } else {
        setMessage("❌ Server error. Make sure Python is running!");
      }
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-container">
        
        {/* Left Side Branding */}
        <div className="register-image-section">
          <img
            src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            alt="Finance Image"
            className="register-brand-icon"
          />
          <h1>Initialize</h1>
          <p>Student Expense Tracker</p>
        </div>
        
        {/* Right Side Form */}
        <div className="register-form-section">
          <form className="register-form" onSubmit={handleRegister}>
            <h2>Create Account</h2>
            
            <div className="register-input-group">
              <input id="fullName" type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
              <label htmlFor="fullName">Full Name</label>
            </div>
            
            <div className="register-input-group">
              <input id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
              <label htmlFor="username">Username</label>
            </div>
            
            <div className="register-input-group">
              <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
              <label htmlFor="email">Email</label>
            </div>
            
            <div className="register-input-group">
              <input id="college" type="text" value={college} onChange={(e) => setCollege(e.target.value)} required />
              <label htmlFor="college">College Name</label>
            </div>
            
            <div className="register-input-group">
              <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              <label htmlFor="password">Password</label>
            </div>
            
            <div className="register-input-group">
              <input id="confirmPassword" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
              <label htmlFor="confirmPassword">Confirm Password</label>
            </div>
            
            {/* Display error/success messages right above the button */}
            {message && <p style={{ color: message.includes('✅') ? '#00ff9d' : '#ff4757', textAlign: 'center', marginBottom: '10px', fontSize: '14px', fontWeight: 'bold' }}>{message}</p>}
            
            <button type="submit" className="register-btn">Register</button>
            
            <p className="register-bottom">
              Already have an account? 
              <Link to="/">Login</Link>
            </p>
            
          </form>
        </div>
      </div>
    </div>
  );
}