import React from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { add_to_cart } from '../actions';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import DownloadButton from "./DownloadButton";
import ReadBookButton from './ReadBookButton';
import { useState } from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';


const Book = ({ book }) => {
  const [open, setOpen] = React.useState(false);

  const dispatch = useDispatch();

  const [ids, setIds] = useState([])

  const saveToBasket = (e) => {
    e.preventDefault();
    //console.log("bookid>>>🤣" + book.id)
    if (ids.indexOf(book.id) === -1) {
      dispatch(add_to_cart(book))
      ids.push(book.id)
    } else {
      alert("Item is already in shopping cart")
    }

    setOpen(true);
  }





  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };



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
        <Typography>Authors: {authors.map((author) => author.name + ", ")}</Typography>
      )
    }

    return (<Typography>Author: {authors[0].name}</Typography>)
  }

  function BookGenres(props) {
    const genres = props.genres;

    if (genres.length > 1) {
      return (
        <Typography>Genres: {genres.map((genre) => genre.name + ", ")}</Typography>
      )
    }

    return (<Typography>Genre: {genres[0].name}</Typography>)

  }


  const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
  });

  return (
    <Card>
      <CardActionArea>
        <Link to={"/books/" + book.id} className="book__link">
          <CardMedia
            component="img"
            height="140"
            image={axios.defaults.baseURL + "/books/" + book.id + "/image/"}
            alt="book"
          />
          <CardContent>
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
        justifyContent: book.price > 0 ? 'center' : 'space-around'
      }}>
        <ActionButton price={book.price} />
      </CardActions>

      <Snackbar open={open} autoHideDuration={3000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          Item is added to shoppingcart!
        </Alert>
      </Snackbar>

    </Card>
  )
}

export default Book
