import React, { useState } from 'react'
import "./Subtotal.css"
import { useSelector } from 'react-redux';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import BuyButton from './BuyButton';

const Subtotal = ({subtotal}) => {
    const shoppingcart = useSelector(state => state.shopping_cart);
    const [prices, setPrices] = useState([])

    return (

        <Card sx={{ minWidth: 400, minHeight: 300 }} className="subtotal">
            <CardContent>
                <Typography>
                    Subtotal:
                    <span>
                        {subtotal} €
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
