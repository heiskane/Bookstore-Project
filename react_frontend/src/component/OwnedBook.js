import React, { useState } from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import DownloadButton from "./DownloadButton";


const OwnedBook = ({ book }) => {

  function BookRating(props) {
    const avg_rating = props.avg_rating;
    // Make nice looking starts or something here
    return (<p>{avg_rating}</p>);
  }

  function BookAuthors(props) {
    const authors = props.authors;

    if (authors.length > 1) {
      return (
        <p>Authors: {authors.map((author) => author.name + " ")}</p>
      )
    }

    return (<p>Author: {authors[0].name}</p>)
  }

  function BookGenres(props) {
    const genres = props.genres;

    if (genres.length > 1) {
      return (
        <p>Genres: {genres.map((genre) => genre.name + " ")}</p>
      )
    }

    return (<p>Genre: {genres[0].name}</p>)

  }

  return (
    <Card className="book">
      <Link to={"/books/" + book.id} className="book__link">
        <CardMedia
          component="img"
          height="340"
          image={axios.defaults.baseURL + "/books/" + book.id + "/image/"}
          alt="book"
        />
      </Link>
      <CardContent className="book__info">
        <Typography>{book.title}</Typography>
        <BookRating avg_rating={book.avg_rating} />
        <BookAuthors authors={book.authors} />
        <BookGenres genres={book.genres} />
        <CardActions>
          <Button
            variant="contained"
            component={Link}
            to={"/read_book/" + book.id}
          >
              Read Book
          </Button>
          <DownloadButton book_id={book.id} />
        </CardActions>
      </CardContent>
    </Card>
  )
}

export default OwnedBook
