import React from 'react';
import axios from 'axios';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'
import jwt from 'jwt-decode';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { set_user } from '../actions';
import "./RegisterForm.css";
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

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
        this.props.signIn(user);
        this.setState({ redirect: '/' });
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
            <Typography variant="h2">Register</Typography>
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
                label="email"
                type="email"
                name="email"
                value={this.state.email}
                onChange={this.handleChange}/>
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

          </Grid>
        </form>
      </Paper>
    )
  }

}


const mapDispatchToProps = (dispatch) => {
  return {
    signIn: (user) => dispatch(set_user(user))
  }
};

export default connect(null, mapDispatchToProps)(withCookies(RegisterForm));
