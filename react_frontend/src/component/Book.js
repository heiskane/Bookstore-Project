import React, { useState } from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { add_to_cart } from '../actions';


const Book = ({ book }) => {

  const shoppingCart = useSelector(state => state.shoppingCart);
  const dispatch = useDispatch();

  const saveToBasket = (e) => {
    e.preventDefault();
    dispatch(add_to_cart(book));
  }

  return (
    <div className="book">
      <img src={axios.defaults.baseURL + "/books/" + book.id + "/image/"} alt="" />
      <div className="book__info">
        <Link to={"/books/" + book.id}>
          <p>Name: {book.title}</p>
        </Link>
        <p>Author: {book.authors.map((author) => <li key={author.name}>{author.name}</li>)}</p>
        <p className="book_price">Price: {book.price}
          <small>€</small>
        </p>
      </div>
      <button type="button" onClick={saveToBasket}>Add to Basket</button>
    </div>
  )
}

export default Book
