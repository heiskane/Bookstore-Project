import React from 'react';
import axios from 'axios';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'

// https://reactjs.org/docs/forms.html
class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
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
    axios.post('http://localhost:8000/login/', new URLSearchParams({
      username: this.state.username,
      password: this.state.password
    }), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then((response) => {
      const { cookies } = this.props;
      cookies.set("jwt_token", response.data.access_token,
        { 
          path: "/",
          sameSite: 'strict' 
        });
      this.setState({ jwt_token: cookies.get("jwt_token") });
    })
    .catch(err => {
      alert("Login failed")
      alert(JSON.stringify(err.response.data.detail))
    })
    event.preventDefault();
  }


  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={this.state.username} onChange={this.handleChange} />
        </label>
        <label>
          Password:
          <input type="password" name="password" value={this.state.password} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Login" />
      </form>
    )
  }

}

export default withCookies(LoginForm);
