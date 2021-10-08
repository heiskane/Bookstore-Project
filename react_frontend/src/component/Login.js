import React from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

const Login = () => {



  return (
    <div>
      <div className="login">
        <h1>Login</h1>
        <LoginForm />
      </div>
      <div className="register">
        <h1>Register</h1>
        <RegisterForm />
      </div>
    </div>
  )
}

export default Login
