import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';
import Header from './component/Header';
import Home from './component/Home';
import Checkout from './component/Checkout';
import Login from './component/Login';
import BookDetails from './component/BookDetails';
import ReadBook from './component/ReadBook';
import Profile from './component/Profile';
import { Redirect } from 'react-router-dom';

import ShoppingCart from './component/ShoppingCart';
import Orders from './component/Orders';
import ThankYou from './component/ThankYou';
import ForgetPassword from './ForgetPassword';

// https://github.com/axios/axios#global-axios-defaults
// Define baseURL for all api calls
if (process.env.NODE_ENV !== 'production') {
  axios.defaults.baseURL = 'http://localhost:8000'
} else {
  axios.defaults.baseURL = 'https://api.hlgbooks.com'
}

document.title = "HLG Books"

function App() {
  return (
    <Router>

      <Switch>
        <Route exact path="/">
          <Header />
          <Home />
        </Route>

        <Route
          path="/mobile"
          component={() => {
            window.location.href = 'https://play.google.com/store/apps/details?id=com.hlg.books';
            return null;
          }}
        />
        <Route path="/checkout">
          <Header />
          <Checkout />
        </Route>
        <Route path="/login">
          <Header />
          <Login />
        </Route>
        <Route path="/register">
          <Header />
          <Login />
        </Route>
        <Route path="/books/:book_id">
          <Header />
          <BookDetails />
        </Route>
        <Route path="/read_book/:book_id">
          <Header />
          <ReadBook />
        </Route>

        <Route path="/shoppingcart">
          <Header />
          <ShoppingCart />
        </Route>

        <Route path="/orders">
          <Header />
          <Orders />
        </Route>

        <Route path="/forgetpassword">
          <Header />
          <ForgetPassword />
        </Route>

        <Route path="/profile">
          <Header />
          <Profile />
        </Route>

        <Route path="/thankyou">
          <Header />
          <ThankYou />
        </Route>

      </Switch>

    </Router>
  );
}

export default App;
