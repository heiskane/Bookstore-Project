import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
//import { store } from './component/store'
import { Provider } from 'react-redux'
import { CookiesProvider } from 'react-cookie';
import { createStore } from 'redux';
import allReducers from './reducers';

const store = createStore(
  allReducers,
  // https://github.com/zalmoxisus/redux-devtools-extension
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

store.subscribe(() => console.log(store.getState()));

ReactDOM.render(
  <Provider store={store}>
    <CookiesProvider>
      <App />
    </CookiesProvider>
  </Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
