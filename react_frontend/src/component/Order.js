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

export default function Order({ order }) {

  console.log(order)
  return (
    <div className="order">
      <Card>
        <h1>{order.title}</h1>

      </Card>
    </div>
  );
}




