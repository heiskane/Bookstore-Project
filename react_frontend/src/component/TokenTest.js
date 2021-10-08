import React, { Component } from 'react';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie'

class TokenTest extends Component {

  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  handleCookie = () => {
    const { cookies } = this.props;
    cookies.set("jwt_token", "test2", { path: "/" });
    this.setState({ jwt_token: cookies.get("jwt_token") });
  };

  render() {
    return (
      <button onClick={this.handleCookie}>asd</button>
    )
  }

}

export default withCookies(TokenTest);