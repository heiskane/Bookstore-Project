import React from "react";
import "./ShoppingCart.css";
import { useSelector } from "react-redux";
import Order from "./Order";
import Subtotal from "./Subtotal";
import { useState, useEffect } from "react";

const ShoppingCart = () => {
  const orders = useSelector((state) => state.shopping_cart);
  const [subtotal, setSubtotal] = useState();

  useEffect(() => {
    let total = 0
    for (let i = 0; i < orders.length; i++) {
      total += orders[i].price
    }
    setSubtotal(total)

  }, [orders]);


  return (
    <div className="shoppingcart">
      <div class="shoppingcart__left">
        <h1 className="shoppingcart__header">Your Shopping Cart</h1>
        <div class="shoppingcart__book">
          {orders.map((order) => (
            <Order
              order={order}
              setSubtotal={setSubtotal}
              key={order.id}
            />
          ))}
        </div>
      </div>
      <div class="shoppingcart__right">
        <Subtotal subtotal={subtotal} />
      </div>
    </div>
  );
};

export default ShoppingCart;
