
import axios from "axios";
import React from "react";
import Book from './Book'

import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";

/*
const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "left",
  color: theme.palette.text.secondary
}));
*/

export default function App() {
  const [books, setBooks] = React.useState(null);


  React.useEffect(() => {
    const instance = axios.create();
    instance.get("/books/")
      .then((response) => {
        setBooks(response.data);
      });
  }, []);

  if (!books) return null;

  // https://reactjs.org/docs/lists-and-keys.html
  // https://dev.to/njdevelopment/help-with-react-map-through-json-data-beh

  return (
    <Box className="books" sx={{ flexGrow: 1 }}>
      <Grid container
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={3}>
        {books.map((book) =>
          <Grid item xs={12} sm={6} md={3} lg={2}>
            <Book book={book} />
          </Grid>
        )}
      </Grid>
    </Box>
  );
}