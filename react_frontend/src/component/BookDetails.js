import React from "react";
import './BookDetails.css'
import axios from "axios";
import { useParams } from "react-router-dom";
import DownloadButton from "./DownloadButton";

export default function BookDetails() {

  const [book, setBook] = React.useState(null); 

  let { book_id } = useParams();

  const baseURL = "http://127.0.0.1:8000"

  React.useEffect(() => {
    axios.get(baseURL + "/books/" + book_id)
      .catch(err => {
        console.log(err);
      })
      .then((response) => {
        if (response) {
          setBook(response.data);
          console.log(book);
        } else {
          console.log("Fetching book failed")
        }
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
        <p>Genres: {genres.map((genre) => genre.name + "")}</p>
      )
    }

    return (<p>Genre: {genres[0].name}</p>)

  }

  return (
      <div className="book_details">
        <img src={baseURL + "/books/" + book_id + "/image/"} alt="Book image" />
        <h2>{book.title}</h2>
        <BookRating avg_rating={book.avg_rating}/>
        <BookAuthors authors={book.authors} />
        <BookGenres genres={book.genres} />
        <p>{book.description}</p>
        <p>Price: {book.price} €</p>
        <p>Language: {book.language}</p>
        <p>Publication Date: {book.publication_date}</p>
        <DownloadButton book_id={book.id} />
      </div>
   );
}




