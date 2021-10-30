import React, { useState } from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { add_to_cart } from '../actions';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DownloadButton from "./DownloadButton";
import ReadBookButton from './ReadBookButton';


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
        <>
          <ReadBookButton book_id={book.id} />
          <DownloadButton book_id={book.id} />
        </>
      )
    }
  }

  function BookAuthors(props) {
    const authors = props.authors;

    if (authors.length > 1) {
      return (
        <Typography>Authors: {authors.map((author) => author.name + " ")}</Typography>
      )
    }

    return (<Typography>Author: {authors[0].name}</Typography>)
  }

  function BookGenres(props) {
    const genres = props.genres;

    if (genres.length > 1) {
      return (
        <Typography>Genres: {genres.map((genre) => genre.name + " ")}</Typography>
      )
    }

    return (<Typography>Genre: {genres[0].name}</Typography>)

  }

  return (
    <Card sx={{
      maxWidth: 345
    }} className="book">
      <CardActionArea>
        <Link to={"/books/" + book.id} className="book__link">
          <CardMedia
            component="img"
            height="140"
            image={axios.defaults.baseURL + "/books/" + book.id + "/image/"}
            alt="book"
          />
          <CardContent className="book__info">
            <Typography variant="h5" component="div">
              {book.title}
            </Typography>
            <BookAuthors authors={book.authors} />
            <BookGenres genres={book.genres} />
            <Typography>
              {"Price: " + book.price + "€"}
            </Typography>
          </CardContent>
        </Link>
      </CardActionArea>
      <CardActions sx={{
        display: 'flex',
        justifyContent: 'space-between' 
      }}>
        <ActionButton price={book.price} />
      </CardActions>
    </Card>
  )
}

export default Book
