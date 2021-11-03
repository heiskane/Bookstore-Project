import React from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './Login.css';

const Login = () => {



  return (
    <div className="login">
      <div className="login__loginForm">
        <LoginForm />
      </div>
     
      <div className="login__middle">
        <div className="login__middleline">
        </div>
        <h1>OR</h1>
        <div className="login__middleline">
        </div>
      </div>

      <div className="login__registerForm">
        <RegisterForm />
      </div>
      
  

    </div>
  )
}

export default Login
