import React from 'react'
import Box from '@mui/material/Box'
import useMediaQuery from '@mui/material/useMediaQuery';
import MobileStoreButton from 'react-mobile-store-button';

import './Home.css'
import Books from './Books'

const Home = () => {
    
    const isMobile = useMediaQuery('(max-width:600px)');
    
    return (
        <>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          marginTop: '50px',
          marginLeft: 'auto',
          marginRight: 'auto',
          maxWidth: '1500px',
        }}>
            {isMobile &&
                <MobileStoreButton
                    store="android"
                    url="https://play.google.com/store/apps/details?id=com.hlg.books"
                    linkProps={{ title: "Get it on Google Play" }}
                />
            }
            <Books />
        </Box>
        </>
    )
}

export default Home
