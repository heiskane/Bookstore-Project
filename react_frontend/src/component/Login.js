import React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './Login.css';

const Login = () => {



  return (
    <Box
      className="login"
      padding="5%"
    >
      <Box padding="5%">
        <LoginForm />
      </Box>
     
      <div className="login__middle">
        <div className="login__middleline">
        </div>
        <h1>OR</h1>
        <div className="login__middleline">
        </div>
      </div>

      <Box padding="5%">
        <RegisterForm />
      </Box>
      
  

    </Box>
  )
}

export default Login
