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
import { CardActionArea } from '@mui/material';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import "./Order.css";

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

export default function Order({ order }) {

  console.log("Order>>>" + order)
  return (

    <Stack spacing={2} className="order">
      <Item>
        <Card className="order__card">
          <CardMedia
            component="img"
            height="140"
            image={axios.defaults.baseURL + "/books/" + order.id + "/image/"}
            alt="green iguana"
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {order.title}
            </Typography>
            Author: {order.authors.map((author) => <li key={author.name}>{author.name}</li>)}
            <Typography>
              {order.price}
            </Typography>
          </CardContent>

        </Card>
      </Item>
    </Stack>
  );
}




