import React from 'react';
import axios from 'axios';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'
import jwt from 'jwt-decode';
import { Redirect, Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { set_user } from '../actions';
import './LoginForm.css'

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

// https://reactjs.org/docs/forms.html
class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      redirectTo: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  handleSubmit(event) {
    const instance = axios.create();
    instance.post('/login/', new URLSearchParams({
      username: this.state.username,
      password: this.state.password
    }), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
      .then((response) => {
        const { cookies } = this.props;
        const jwt_token = response.data.access_token
        cookies.set("jwt_token", jwt_token,
          {
            path: "/",
            sameSite: 'strict'
          });
        this.setState({ jwt_token: cookies.get("jwt_token") });
        const user_token = jwt(jwt_token);
        this.props.signIn(user_token);
        this.setState({ redirect: '/' });
      })
      .catch(err => {
        alert((err.response) ? JSON.stringify(err.response.data.detail) : "Login failed")
        console.log(err)
      })
    event.preventDefault();
  }


  render() {
    if (this.state.redirect) {
      return <Redirect to={this.state.redirectTo} />
    }
    return (
      <Paper
        elevation={8}
      >
        <form
          onSubmit={this.handleSubmit}
        >
          <Grid
            container
            flexDirection='column' 
            justifyContent='center'
            alignItems='center'
            padding={10}
            spacing={2}
          >
            <Typography variant="h2">Login</Typography>
            <Grid item>
              <TextField
                label="Username"
                type="text"
                name="username"
                required
                value={this.state.username}
                onChange={this.handleChange} />
            </Grid>

            <Grid item>
              <TextField
                label="Password"
                type="password"
                name="password"
                value={this.state.password}
                onChange={this.handleChange} />
            </Grid>

            <Grid item>
              <Button type="submit" variant="contained">Login</Button>
            </Grid>

            <Link to="/forgetPassword" className="loginForm__forgetPassword">
              Forgot password?
            </Link>

          </Grid>
        </form>
      </Paper>
    )
  }

}

const mapDispatchToProps = (dispatch) => {
  return {
    signIn: (user_token) => dispatch(set_user(user_token))
  }
};

export default connect(null, mapDispatchToProps)(withCookies(LoginForm));
