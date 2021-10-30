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
import DownloadButton from "./DownloadButton";


const Book = ({ book }) => {

  const shoppingCart = useSelector(state => state.shoppingCart);
  const dispatch = useDispatch();

  const saveToBasket = (e) => {
    e.preventDefault();
    dispatch(add_to_cart(book));
  }

  function ActionButton(props) {
    if (props.price > 0) {
      return (
        <Button 
          type="submit"
          variant="contained"
          onClick={saveToBasket}
        >
          Add to Cart
        </Button>
      )
    } else {
      return (
        <CardActions>
          <Button
            variant="contained"
            component={Link}
            to={"/read_book/" + book.id}
          >Read
          </Button>
          <DownloadButton book_id={book.id} />
        </CardActions>
      )
    }
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
      <ActionButton price={book.price} />
    </Card>
  )
}

export default Book
