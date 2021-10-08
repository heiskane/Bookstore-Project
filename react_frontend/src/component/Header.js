import { Link } from 'react-router-dom'
import React from 'react'
import './Header.css'
import SearchIcon from '@material-ui/icons/Search';
import { ShoppingBasket } from '@material-ui/icons';
import HLG_Books from '../photos/HLG_Books.png'
import { useCookies } from 'react-cookie';
import jwt from 'jwt-decode';

const Header = () => {
  const [cookies, setCookie, removeCookie] = useCookies();
  
  const handleAuthentication = () => {

  }

  function handleLogout() {
    removeCookie("jwt_token");
  }

  const LoginOrUser = () => {
    if (!cookies.jwt_token) {
      return (
        <Link to="/login" className="header__link">
          <div
            className="header__option"
            onClick={handleAuthentication}
          >
            <span className="header__optionLineOne">Hello Guest</span>
            <span className="header__optionLineTwo">Sign In</span>
          </div>
        </Link>
      )
    } else {
      const username = jwt(cookies.jwt_token).sub
      return (
        <div className="header__nav">
          <Link to="/">
            <div className="header__option">
              <span className="header__optionLineOne">{"Hello " + username}</span>
              <span className="header__optionLineTwo">This will be you profile button</span>
            </div>
          </Link>
          <Link to="/login" onClick={() => handleLogout()}>
            <div className="header__option">
              <span className="header__optionLineTwo">Logout</span>
            </div>
          </Link>
        </div>
      )
    }
  }

  return (
    <div className="header">

      {/* logo on the left -> img */}
      {/* Search box */}
      {/* 3 links */}
      {/* Shopping Basket icon with number */}

      <Link to="/">
        <img className="header__logo" src={HLG_Books} alt="HLG_Books logo" />
      </Link>

      <div className="header__search">
        <input type="text" className="header__searchInput" />
        <SearchIcon className="header__searchIcon"></SearchIcon>
      </div>

      <div className="header__nav">
        <LoginOrUser />


        <div className="header__option">
          <span className="header__optionLineOne">Returns</span>
          <span className="header__optionLineTwo">&Oders</span>
        </div>


        <div className="header__optionBasket">
          <ShoppingBasket />
          <span className="header__optionLineTwo header__basketCount">0</span>
        </div>

      </div>
    </div>
  )
}

export default Header
