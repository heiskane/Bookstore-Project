import { Link } from 'react-router-dom'
import React from 'react'
import './Header.css'
import SearchIcon from '@material-ui/icons/Search';
import { ShoppingBasket } from '@material-ui/icons';
import HLG_Books from '../photos/HLG_Books.png'
import { useCookies } from 'react-cookie';
import { useSelector, useDispatch } from 'react-redux';
import { unset_user } from '../actions';

const Header = () => {
  const [cookies, setCookie, removeCookie] = useCookies();
  const user_token = useSelector(state => state.user_token)
  const dispatch = useDispatch();

  const handleAuthentication = () => {

  }

  function handleLogout() {
    // https://stackoverflow.com/questions/54861709/cookies-removeabc-not-working-in-reactjs/55593030
    removeCookie("jwt_token", { path: '/' });
    dispatch(unset_user());
  }

  const LoginOrUser = () => {
    if (!user_token.sub) {
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
      return (
        <div className="header__nav">
          <Link to="/">
            <div className="header__option">
              <span className="header__optionLineOne">
                {"Hello " + user_token.sub}
              </span>
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

        <Link to="/shoppingcart">

          <div className="header__optionBasket">

            <ShoppingBasket />
            <span className="header__optionLineTwo header__basketCount">0</span>

          </div>
        </Link>
      </div>
    </div>
  )
}

export default Header
