import React from 'react';
import axios from 'axios';

// https://reactjs.org/docs/forms.html
export default class RegisterForm extends React.Component {
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

  handleSubmit(event) {
    axios.post('http://localhost:8000/users/', {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password
    })
    .then((response) => {
      alert("User created successfully")
    })
    .catch(err => {
      alert("Registeration failed")
      alert(JSON.stringify(err.response.data.detail))
    })
    event.preventDefault();
  }


  render() {
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


