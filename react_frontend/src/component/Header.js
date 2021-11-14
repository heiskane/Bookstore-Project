import { Link } from 'react-router-dom'
import React, { useEffect } from 'react'
import './Header.css'
//import HLG_Books from '../photos/HLG_Books.png'
import { useCookies } from 'react-cookie';
import { useSelector, useDispatch } from 'react-redux';
import { unset_user, set_user } from '../actions';
import jwt from 'jwt-decode';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import Box from '@mui/material/Box'
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';

const Header = () => {
  // This seems to give 'removeCookies' as the third option
  // Do 'cookies' AND 'setCookies' have to be included as well
  const [cookies, setCookie, removeCookie] = useCookies();
  const user_token = useSelector(state => state.user_token)
  const dispatch = useDispatch();
  const shoppingcart = useSelector(state => state.shopping_cart);

  useEffect(() => {
    if (cookies.jwt_token) {
      dispatch(set_user(jwt(cookies.jwt_token)));
    }
  }, []);


  function handleLogout(e) {
    // https://stackoverflow.com/questions/54861709/cookies-removeabc-not-working-in-reactjs/55593030
    e.preventDefault();
    removeCookie("jwt_token", { path: '/' });
    dispatch(unset_user());
  }

  const LoginOrUser = () => {
    if (!user_token.sub) {
      return (
        <Button
          color='inherit'
          component={Link}
          to="/login"
        >
          Login
        </Button>
      )
    } else {
      return (
        <>
          <Button
            color='inherit'
            //onClick={() => alert("Profile page not yet implemented")}
            component={Link}
            to="/profile"
          >
            {user_token.sub}
          </Button>

          <Button
            color='inherit'
            component={Link}
            to="/orders"
          >My Books</Button>

          <Button
            color='inherit'
            onClick={handleLogout}
            component={Link}
            to="/login"
          >
            Logout
          </Button>
        </>
      )
    }
  }

  return (
    <Box sx={{ flexGrow: 1 }}>

      <AppBar position='static'>

        {/*
      <Link to="/">
        <img className="header__logo" src={HLG_Books} alt="HLG_Books logo" />
      </Link>
      */}
        <Toolbar>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'inherit'
            }}>
            HLG Bookstore
          </Typography>

          <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
            <LoginOrUser />
            <IconButton
              color="inherit"
              component={Link}
              to="/shoppingcart"
            >
              <Badge
                sx={{ overflow: 'visible' }}
                overlap="circular"
                badgeContent={shoppingcart.length}
                color="error">
                <ShoppingCartOutlinedIcon />
              </Badge>
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  )
}

export default Header
