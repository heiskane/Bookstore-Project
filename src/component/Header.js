import { Link } from 'react-router-dom'
import React from 'react'
import './Header.css'
import SearchIcon from '@material-ui/icons/Search';

const Header = () => {
    return (
        <nav className="header">
         
            {/* logo on the left -> img */}
            {/* Search box */}
            {/* 3 links */}
            {/* Shopping Basket icon with number */}

            <Link to="/">
                <img className="header__logo" src='https://d24v5oonnj2ncn.cloudfront.net/wp-content/uploads/2018/10/16030301/Amazon-Logo-Black.jpg' alt="QiBook store logo" />
            </Link>

            <div class="header__search">
                <input type="text" className="header__searchInput" />
                <SearchIcon className="header__searchIcon"></SearchIcon>
            </div>

            <div class="header__nav">
                
            </div>
        </nav>
    )
}

export default Header
