import React, { useState } from 'react';
import axios from 'axios';
import './FormStyles.css';

function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Sending login to:", `${process.env.REACT_APP_API_URL}/login`);

      const res = await axios.post(`${process.env.REACT_APP_API_URL}/login`, {
        username,
        password
      },{
        headers : {
      "Content-Type": "application/json"

      },
      
        withCredentials: true
      });
      localStorage.setItem("token", res.data.token);
      onLogin();
    } catch (err) {
      console.error("Login error:", err);
      alert("Login failed");
    }
  };

  return (
    <div className="form-container">
    <div className="company-name">
      {/* <span className="purple">PURPLERAIN</span> <span className="white">TECHSAFE</span> */}
    </div>
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form></div>
  );
}

export default LoginForm;
