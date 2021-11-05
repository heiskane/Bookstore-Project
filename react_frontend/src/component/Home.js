import React from 'react'
import Box from '@mui/material/Box'

import './Home.css'
import Books from './Books'

const Home = () => {
    return (
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          marginTop: '50px',
          marginLeft: 'auto',
          marginRight: 'auto',
          maxWidth: '1500px',
        }}>
            <Books />
        </Box>
    )
}

export default Home
