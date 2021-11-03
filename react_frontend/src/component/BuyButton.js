import React from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { useSelector, useDispatch } from "react-redux";
import { useState, useEffect } from "react";
import { useCookies } from 'react-cookie';

const BuyButton = () => {
	const dispatch = useDispatch();
	const [cookies] = useCookies();

	const shoppingCart = useSelector(state => state.shopping_cart);
	const [ids, setIds] = useState([])

	useEffect(() => {
		shoppingCart?.map((item) => { ids.push(item.id) })
		console.log("ids in the BuyButton>>><" + ids)
	}, [])

	return (
		<PayPalScriptProvider options={
			{
				"client-id": "AVRE2PhqcdO4hh6ak49te0ouOyRq3cdngOheyPvCqS7QQew1XOykcvEM4L9X3DGyWRDnyhGsCZtUg62m",
				"currency": "EUR"
			}
		}>
			<PayPalButtons
				style={{ layout: "horizontal" }}
				createOrder={(data, actions) => {
					return fetch('http://localhost:8000/checkout/paypal/order/create/', {
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
					return fetch('http://localhost:8000/checkout/paypal/order/' + data.orderID + '/capture/', {
						method: 'post',
						headers: {
							'Authorization': 'Bearer ' + cookies.jwt_token
						}
					}).then(
						dispatch({ type: 'EMPTY_SHOPPINGCART' })
					).then(function (orderData) {
						console.log(orderData);
					});
				}} // TODO: If user not logged in set jwt_token from response

				onError={(error) => {
					alert("Something went wrong :(")
				}}
			/>
		</PayPalScriptProvider>
	);

}

export default BuyButton;