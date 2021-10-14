import React, { useState, useEffect } from 'react'
import "./Subtotal.css"
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import shoppingCart from '../reducers/shoppingCart';
import BuyButton from './BuyButton';

const Subtotal = () => {
    const shoppingcart = useSelector(state => state.shopping_cart);
    const [prices, setPrices] = useState([])

    return (

        <Card sx={{ minWidth: 400, minHeight: 300 }} className="subtotal">
            <CardContent>
                <Typography>
                    Subtotal:
                    <span>
                        {shoppingcart?.map((book) => { prices.push(book.price) })}
                        {prices?.reduce((accumulator, currentValue) => {
                            return accumulator + currentValue;
                        }, 0)} €
                    </span>

                </Typography>
            </CardContent>
            {/* checkout button */}
            <CardActions>
                <span>Safe Pay with</span>
                <BuyButton />
            </CardActions>

        </Card>

    )
}

export default Subtotal
