import React from 'react'
import "./ShoppingCart.css"
import { useSelector, useDispatch } from 'react-redux';
import Order from './Order'
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const bull = (
    <Box
        component="span"
        sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
    >
        •
    </Box>
);

const ShoppingCart = () => {
    const orders = useSelector(state => state.shopping_cart);
    // console.log("FROM SHOPPINGCART>>>" + orders)

    return (
        <div className="shoppingcart">
            <div class="shoppingcart__left">
                <h1 className="shoppingcart__header">Your Shopping Cart</h1>
                <div class="shoppingcart__book">
                    {
                        orders.map((order) => <Order order={order} />)
                    }
                </div>
            </div>

            <Card class="shoppingcart__right" sx={{ minWidth: 275 }}>
                <CardContent>
                    <Typography>
                        Subtotal
                    </Typography>
                    <Typography>
                        €
                    </Typography>
                </CardContent>
                {/* checkout button */}
                <CardActions>
                    <Button size="small">Proceed to Checkout</Button>
                </CardActions>
            </Card>
        </div>
    )
}

export default ShoppingCart
