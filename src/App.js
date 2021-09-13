import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Header from './component/Header';

import Home from './component/Home';
function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/">
            <Header />

            <Home />
          </Route>
        </Switch>

      </div>

    </Router>
  );
}

export default App;
