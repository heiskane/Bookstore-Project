import React, { useState } from 'react'
import "./Subtotal.css"
import { useSelector } from 'react-redux';
import { useCookies } from 'react-cookie';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import BuyButton from './BuyButton';

const Subtotal = ({ subtotal }) => {

    const [cookies, setCookie, removeCookie] = useCookies();

    return (

        <Card sx={{ minWidth: 400, minHeight: 300 }} className="subtotal">
            <CardContent>
                <Typography>
                    Subtotal:
                    <span>
                        {subtotal} €
                    </span>
                </Typography>
                {!cookies.jwt_token &&
                <Typography>
                    We strongly recommend registering a user before buying books
                    so that they are added to your account.
                </Typography>
                }
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
