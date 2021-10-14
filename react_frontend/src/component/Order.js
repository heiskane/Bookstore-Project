import React from "react";
import './BookDetails.css'
import axios from "axios";
import { useParams } from "react-router-dom";
import DownloadButton from "./DownloadButton";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Button } from '@mui/material';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import "./Order.css";
import DeleteIcon from '@mui/icons-material/Delete';

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));


export default function Order({ order }) {

  console.log("Order>>>" + order)
  return (

    <Card className="order__card" sx={{ display: 'flex', maxWidth: 500, borderBottom: '1px solid grey' }} >
      <CardMedia
        className="order__cardMedia"
        component="img"
        height="200"
        sx={{ width: 250 }}
        image={axios.defaults.baseURL + "/books/" + order.id + "/image/"}
        alt="book cover"
      />
      <CardContent
        className="order__cardContent"
      >
        <Typography gutterBottom variant="h5" component="div">
          {order.title}
        </Typography>
        Author: {order.authors.map((author) => <li key={author.name}>{author.name}</li>)}
        <Typography>
          {order.price} €
        </Typography>
      </CardContent>

      <CardActions className="order__delete" >
        <Button
          size="small"
          variant="contained"
          startIcon={<DeleteIcon />}>
          DELETE
        </Button>
      </CardActions>
    </Card>

  );
}




