import React, { useState } from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { add_to_cart } from '../actions';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';

const Book = ({ book }) => {

  const shoppingCart = useSelector(state => state.shoppingCart);
  const dispatch = useDispatch();

  const saveToBasket = (e) => {
    e.preventDefault();
    dispatch(add_to_cart(book));
  }

  return (
    <Card sx={{ maxWidth: 345 }} className="book">
      <Link to={"/books/" + book.id} className="book__link">
        <CardMedia
          component="img"
          height="140"
          image={axios.defaults.baseURL + "/books/" + book.id + "/image/"}
          alt="book"
        />
        <CardContent className="book__info">

          <Typography>{book.title}</Typography>

          <p>Author: {book.authors.map((author) => <li key={author.name}>{author.name}</li>)}</p>
          <p className="book_price">Price: {book.price}
            <small>€</small>
          </p>
        </CardContent>
      </Link>
      {/*  <button type="button" onClick={saveToBasket}>Add to Basket</button> */}
      <Button type="submit" variant="contained" onClick={saveToBasket}>Add to basekt</Button>
    </Card>
  )
}

export default Book
