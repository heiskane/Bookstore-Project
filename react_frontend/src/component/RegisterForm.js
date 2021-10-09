import React from 'react';
import axios from 'axios';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'
import jwt from 'jwt-decode';
import { Redirect } from 'react-router-dom';

// https://reactjs.org/docs/forms.html
class RegisterForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      email: '',
      password: ''
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
    instance.post('/users/', {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password
    })
    .then((response) => {
      alert("User created successfully")
      const { cookies } = this.props;
      const jwt_token = response.data.access_token
      cookies.set("jwt_token", jwt_token,
        {
          path: "/",
          sameSite: 'strict' 
        });
      this.setState({ jwt_token: cookies.get("jwt_token") });
      const user = jwt(jwt_token);
      console.log(user);
      this.setState({ redirect: '/'});
    })
    .catch(err => {
      alert("Registeration failed")
      alert(JSON.stringify(err.response.data.detail))
    })
    event.preventDefault();
  }


  render() {
    if (this.state.redirect) {
      return <Redirect to={this.state.redirectTo} />
    }
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Username:
          <input 
            type="text" name="username" value={this.state.username}
            onChange={this.handleChange} />
        </label>
        <label>
          Email:
          <input type="email" name="email" value={this.state.email}
          onChange={this.handleChange} />
        </label>
        <label>
          Password:
          <input type="password" name="password" value={this.state.password}
          onChange={this.handleChange} />
        </label>
        <input type="submit" value="Login" />
      </form>
    )
  }

}

export default withCookies(RegisterForm);
