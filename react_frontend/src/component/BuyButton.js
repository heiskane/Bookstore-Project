import React from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { useSelector, useDispatch } from "react-redux";
import { useState, useEffect } from "react";
import { useCookies } from 'react-cookie';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

import { download_book } from './DownloadFunc';

const BuyButton = () => {
  const dispatch = useDispatch();

  const [cookies, setCookie] = useCookies();
  const [redirect, setRedirect] = useState(false);

  const shoppingCart = useSelector(state => state.shopping_cart);
  const [ids, setIds] = useState([])

  useEffect(() => {
    shoppingCart?.map((item) => { ids.push(item.id) })
  }, [])

  function PayPalBuyButton() {
    return (

      <PayPalButtons
        style={{ layout: "horizontal" }}
        createOrder={(data, actions) => {
          return fetch(axios.defaults.baseURL + '/checkout/paypal/order/create/', {
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + cookies.jwt_token
            },
            body: JSON.stringify(
              { "book_ids": ids }
            )
          })
            .then((res) => {
              if (!res.ok) {
                throw new Error('Something went wrong');
              } else {
                return res.json();
              }
            })
            .then(function (orderData) {
              // Maybe deal with this server-side
              return orderData.result.id;
            });
        }}

        onApprove={(data, actions) => {
          return fetch(axios.defaults.baseURL + '/checkout/paypal/order/' + data.orderID + '/capture/', {
            method: 'post'
          })
          .then(
            dispatch({ type: 'EMPTY_SHOPPINGCART' })
          )
          .then((res) => {
            return res.json();
          })
          .then((json) => {
            //console.log(json);
            if (!cookies.jwt_token) {
              setCookie("jwt_token", json.access_token,
                {
                  path: "/",
                  sameSite: 'strict'
                });
              for (let i = 0; i < ids.length; i++) {
                download_book(ids[i], json.access_token);
              }
            }
            setRedirect(true);
          });
        }}

        onError={(error) => {
          alert("Something went wrong :(")
        }}
      />
    )
  }

  if (redirect) {
    return (
      <Redirect to="/thankyou" />
    )
  }

  if (process.env.NODE_ENV !== 'production') {
    return (
      <PayPalScriptProvider options={
        {
          "client-id": "AVRE2PhqcdO4hh6ak49te0ouOyRq3cdngOheyPvCqS7QQew1XOykcvEM4L9X3DGyWRDnyhGsCZtUg62m",
          "currency": "EUR"
        }
      }>
        <PayPalBuyButton />
      </PayPalScriptProvider>
    );
  } else {
    return (
      <PayPalScriptProvider options={
        {
          "client-id": "ARBTnyC9yOG3m5nkySbFD8E453_QsA-f24Y_xnlB9bgR2JApJtkArLZ5xE4S0yTTfSCx_cAe2DqNJvh0",
          "currency": "EUR"
        }
      }>
        <PayPalBuyButton />
      </PayPalScriptProvider>
    );
  }

}

export default BuyButton;