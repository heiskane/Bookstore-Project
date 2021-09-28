import React from "react";
import axios from "axios";

export default function BookDetails() {
  const [book, setBook] = React.useState(null); 
  React.useEffect(() => {
    axios.get("http://127.0.0.1:8000/books/1")
      .then((response) => {
        setBook(response.data);
        console.log(book);    
      });
  }, []);
  if (!book) return null;
  return (
      <h1>{book.title}</h1>
   );
}




