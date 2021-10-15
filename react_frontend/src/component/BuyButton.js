import React from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

export default class BuyButton extends React.Component {
	render() {
		return (
			<PayPalScriptProvider options={
				{ 
					"client-id": "AVRE2PhqcdO4hh6ak49te0ouOyRq3cdngOheyPvCqS7QQew1XOykcvEM4L9X3DGyWRDnyhGsCZtUg62m",
					"currency": "EUR"
				}
			}>
				<PayPalButtons
					style = {{ layout: "horizontal" }}
					createOrder = {(data, actions) => {
						return fetch('http://localhost:8000/checkout/paypal/order/create/', {
							method: 'post',
							headers: { 'Content-Type': 'application/json' },
							body: JSON.stringify(
								{ "book_ids": [11, 12] } // Put book IDs here from shopping cart
							)
						}).then(function(res) {
							return res.json();
						}).then(function(orderData) {
							// Maybe deal with this server-side
							return orderData.result.id;
						});
					}}

					onApprove = {(data, actions) => {		
						return fetch('http://localhost:8000/checkout/paypal/order/' + data.orderID + '/capture/', {
							method: 'post'
						}).then(function(res) {
							return res.json();
						}).then(function(orderData) {
							console.log(orderData);
						});
					}} // TODO: If user not logged in set jwt_token from response
				/>
			</PayPalScriptProvider>
		);
  }
}