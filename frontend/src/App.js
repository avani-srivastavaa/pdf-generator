import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import GenerateForm from './components/GenerateForm';
import './App.css'; // Import styles

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div className="page-wrapper">
      <h1 className="brand-title">
        <span className="purple">PURPLERAIN</span> <span className="white">TECHSAFE</span>
      </h1>
      <div className="form-wrapper">
        {loggedIn ? (
          <GenerateForm />
        ) : (
          <LoginForm onLogin={() => setLoggedIn(true)} />
        )}
      </div>
    </div>
  );
}

export default App;
