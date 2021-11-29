import React from 'react'
import "./Subtotal.css"
import { useCookies } from 'react-cookie';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import BuyButton from './BuyButton';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { useEffect } from "react";

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});


const Subtotal = ({ subtotal }) => {
    const [open, setOpen] = React.useState(false);

    const handleClick = () => {
        setOpen(true);
    };

    useEffect(() => {
        setOpen(true)
    }, [subtotal])

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };


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
            <Snackbar open={open} autoHideDuration={2000} onClose={handleClose}>
                <Alert onClose={handleClose} severity="info" sx={{ width: '100%' }}>
                    Item is deleted!
                </Alert>
            </Snackbar>
        </Card>

    )
}

export default Subtotal
