import React from 'react';
import axios from 'axios';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'
import jwt from 'jwt-decode';
import { Redirect } from 'react-router-dom';
import { connect, useDispatch } from 'react-redux';
import { set_user, unset_user } from '../actions';
import './LoginForm.css'
import Button from '@mui/material/Button';
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
      <form
        className="loginForm"
        onSubmit={this.handleSubmit}>
        <label className="loginForm__lable">
          Username:
          <span>
            <input type="text" name="username" value={this.state.username} onChange={this.handleChange} />
          </span>
        </label>
        <label className="loginForm__lable">
          Password:
          <span>
            <input type="password" name="password" value={this.state.password} onChange={this.handleChange} />
          </span>
        </label>
        <Button type="submit" variant="contained">Login</Button>
      </form>
    )
  }

}

const mapDispatchToProps = (dispatch) => {
  return {
    signIn: (user_token) => dispatch(set_user(user_token))
  }
};

export default connect(null, mapDispatchToProps)(withCookies(LoginForm));
