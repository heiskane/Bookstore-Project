import React from 'react'
import Book from './Book'
import './Home.css'

const Home = () => {
    return (
        <div className="home">
            <div class="home__container">
                <img className="home__image" src="https://s2.adlibris.com/images/61500292/promo1280x270.jpg" alt=" " />
            </div>
            <div class="home__row">
                {/*  Six books */}
                <Book />
                <Book />
                <Book />
                <Book />
                <Book />
                <Book />
            </div>

            <div class="home__row">
                {/*  Six books */}
                <Book />
                <Book />
                <Book />
                <Book />
                <Book />
                <Book />
            </div>

        </div>
    )
}

export default Home
