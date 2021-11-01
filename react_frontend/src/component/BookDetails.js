import React from "react";
import './BookDetails.css'
import axios from "axios";
import { useParams } from "react-router-dom";
import DownloadButton from "./DownloadButton";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import ReadBookButton from './ReadBookButton';

export default function BookDetails() {

  const [book, setBook] = React.useState(null);
  let { book_id } = useParams();
  const instance = axios.create();

  React.useEffect(() => {
    instance.get("/books/" + book_id)
      .then((response) => {
        if (response) {
          setBook(response.data);
          console.log(book);
        } else {
          console.log("Fetching book failed")
        }
      })
      .catch(err => {
        console.log(err);
      });
  }, []);

  if (!book) return null;

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
    <Box sx={{
      display: 'flex',
      justifyContent: 'center'
    }}>
      <Card  sx={{
        maxWidth: 600,
        maxHeight: "100vh"
      }} className="book">
        <CardMedia
          component="img"
          height="340px"
          image={axios.defaults.baseURL + "/books/" + book_id + "/image/"}
          alt="Book cover"
        />
        <Typography  variant="h5" component="div">
          {book.title}
        </Typography>
        <BookRating avg_rating={book.avg_rating} />
        <BookAuthors authors={book.authors} />
        <BookGenres genres={book.genres} />
        <Typography>Description: {book.description}</Typography>
        <Typography>Price: {book.price} €</Typography>
        <Typography>Language: {book.language}</Typography>
        <Typography>Publication Date: {book.publication_date}</Typography>
        <CardActions sx={{
          display: 'flex',
          justifyContent: 'space-between' 
        }}>
          <ReadBookButton book_id={book.id} />
          <DownloadButton book_id={book.id} />
        </CardActions>
      </Card>
    </Box>
  );
}




