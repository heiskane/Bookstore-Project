import React from 'react'
import "./ShoppingCart.css"
import { useSelector, useDispatch } from 'react-redux';
import Order from './Order'

const ShoppingCart = () => {
    const orders = useSelector(state => state.shopping_cart);
    //console.log("FROM SHOPPINGCART>>>" + shopping_cart)

    return (
        <div>
            <h1>Your Orders</h1>
            {
                orders.map((order) => <Order order={order} />)
            }
        </div>
    )
}

export default ShoppingCart
