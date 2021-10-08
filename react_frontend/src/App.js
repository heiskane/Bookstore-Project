import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Header from './component/Header';
import Home from './component/Home';
import Checkout from './component/Checkout';
import Login from './component/Login';
import BookDetails from './component/BookDetails'

import axios from 'axios';

// https://github.com/axios/axios#global-axios-defaults
// Define baseURL for all api calls
axios.defaults.baseURL = 'http://localhost:8000'

function App() {
  return (
    <Router>
      <div className="app">

        <Switch>
          <Route exact path="/">
            <Header />
            <Home />
          </Route>

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
        </Switch>

      </div>

    </Router>
  );
}

export default App;
