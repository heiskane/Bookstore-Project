import React from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './Login.css';
import Box from '@mui/material/Box';

const Login = () => {



  return (
    <div className="login">
      <LoginForm />
      <div className="login__middle">
        <div className="login__middleline">
        </div>
        <h1>OR</h1>
        <div className="login__middleline">
        </div>
      </div>
      
      <RegisterForm />

    </div>
  )
}

export default Login
