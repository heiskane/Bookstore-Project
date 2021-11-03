import React from "react";
import "./ShoppingCart.css";
import { useSelector } from "react-redux";
import Order from "./Order";
import Box from "@mui/material/Box";
import Subtotal from "./Subtotal";
import { useState, useEffect } from "react";

const bull = (
  <Box
    component="span"
    sx={{ display: "inline-block", mx: "2px", transform: "scale(0.8)" }}
  >
    •
  </Box>
);

const ShoppingCart = () => {
  const orders = useSelector((state) => state.shopping_cart);
  const [prices, setPrices] = useState([]);

 
  useEffect(() => {
    {
      orders?.map((book) => {
        prices.push(book.price);
      });
    }
  }, [orders]);

    const subtotal = prices.reduce((accumulator, currentValue) => {
        return accumulator + currentValue;
    }, 0);


  return (
    <div className="shoppingcart">
      <div class="shoppingcart__left">
        <h1 className="shoppingcart__header">Your Shopping Cart</h1>
        <div class="shoppingcart__book">
          {orders.map((order) => (
            <Order order={order} />
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
