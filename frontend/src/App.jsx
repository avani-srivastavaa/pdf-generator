
import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import GenerateForm from './components/GenerateForm';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  return (
    <div>{loggedIn ? <GenerateForm /> : <LoginForm onLogin={() => setLoggedIn(true)} />}</div>
  );
}
export default App;
