import React from 'react';
import './Book.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import DownloadButton from './DownloadButton';
import ReadBookButton from './ReadBookButton';


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
      <CardActionArea>
        <Link
          to={"/books/" + book.id} className="book__link">
          <CardMedia
            component="img"
            height="340"
            image={axios.defaults.baseURL + "/books/" + book.id + "/image/"}
            alt="book"
          />
          <CardContent className="book__info">
            <Typography>{book.title}</Typography>
            <BookRating avg_rating={book.avg_rating} />
            <BookAuthors authors={book.authors} />
            <BookGenres genres={book.genres} />
          </CardContent>
        </Link>
      </CardActionArea>
      <CardActions sx={{
        display: 'flex',
        justifyContent: 'space-between' 
      }}>
        <ReadBookButton book_id={book.id} />
        <DownloadButton book_id={book.id} />
      </CardActions>
    </Card>
  )
}

export default OwnedBook
