import React from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './Login.css';
import Box from '@mui/material/Box';

const Login = () => {



  return (
    <div className="login">
      <Box
        className="login__login"
        sx={{
          width: 300,
          height: 300,
        }}
      >
        <h1>Login</h1>
        <LoginForm />
      </Box>
      <div className="login__middle">
        <div className="login__middleline">
        </div>
        <h1>OR</h1>
        <div className="login__middleline">
        </div>
      </div>
      <Box
        className="login__register"
        sx={{
          width: 300,
          height: 300,
        }}
      >
        <h1>Register</h1>
        <RegisterForm />
      </Box>
    </div>
  )
}

export default Login
