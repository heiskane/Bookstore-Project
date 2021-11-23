import React from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { useSelector, useDispatch } from "react-redux";
import { useState, useEffect } from "react";
import { useCookies } from 'react-cookie';
import axios from 'axios';

const BuyButton = () => {
  const dispatch = useDispatch();
  const [cookies, setCookie] = useCookies();

  const shoppingCart = useSelector(state => state.shopping_cart);
  const [ids, setIds] = useState([])

  /*
  if (process.env.NODE_ENV != 'production') {
    setClientId("AVRE2PhqcdO4hh6ak49te0ouOyRq3cdngOheyPvCqS7QQew1XOykcvEM4L9X3DGyWRDnyhGsCZtUg62m");
  } else {
    setClientId("ARBTnyC9yOG3m5nkySbFD8E453_QsA-f24Y_xnlB9bgR2JApJtkArLZ5xE4S0yTTfSCx_cAe2DqNJvh0");
  }*/

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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
              { "book_ids": ids } // Put book IDs here from shopping cart
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
            method: 'post',
            headers: {
              'Authorization': 'Bearer ' + cookies.jwt_token
            }
          })
          .then(
            dispatch({ type: 'EMPTY_SHOPPINGCART' })
          )
          .then((res) => {
            return res.json();
          })
          .then((json) => {
            console.log(json);
            if (!cookies.jwt_token) {
              setCookie("jwt_token", json.access_token,
                {
                  path: "/",
                  sameSite: 'strict'
                });
            }
          });
        }} // TODO: If user not logged in set jwt_token from response

        onError={(error) => {
          alert("Something went wrong :(")
        }}
      />
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