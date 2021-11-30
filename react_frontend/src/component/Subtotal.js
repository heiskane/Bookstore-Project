import React from 'react'
import "./Subtotal.css"
import { useCookies } from 'react-cookie';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import BuyButton from './BuyButton';

const Subtotal = ({ subtotal }) => {


    const [cookies] = useCookies();

    return (

        <Card sx={{ minWidth: 400, minHeight: 300, backgroundColor: '#1976d2' }} className="subtotal">
            <CardContent>
                <Typography gutterBottom variant="h4" component="div" sx={{ color: '#fff' }}>
                    Subtotal: {subtotal} €
                </Typography>
                {!cookies.jwt_token &&
                    <Typography>
                        We strongly recommend registering a user before buying books
                        so that they are added to your account.
                    </Typography>
                }
            </CardContent>
            {/* checkout button */}
            <CardActions sx={{ color: '#fff' }}>
                <span>Safe Pay with</span>
                <BuyButton />
            </CardActions>

        </Card>

    )
}

export default Subtotal
