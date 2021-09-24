
import axios from "axios";
import React from "react";
import Book from './Book'

const baseURL = "http://localhost:8000";

export default function App() {
  const [books, setBooks] = React.useState(null);

  React.useEffect(() => {
    axios.get(baseURL + "/books")
      .then((response) => {
        setBooks(response.data);
        console.log(books)
      });
  }, []);

  if (!books) return null;

  // https://reactjs.org/docs/lists-and-keys.html
  // https://dev.to/njdevelopment/help-with-react-map-through-json-data-beh

  return (
    <div className="books">
      {/* <h1>Books</h1>
      {books.map((book) => [
        <p>Title: {book.title}</p>,
        <p>Description: {book.description}</p>,
        <p>Authors: {book.authors.map((author) => author.name)}</p>,
        <p>Publication Date: {book.publication_date}</p>,
        <br />
      ])} */}

      {books.map((book) => <Book book={book} />)}

    </div>
  );
}