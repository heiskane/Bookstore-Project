import React from 'react'
import './Home.css'
import Books from './Books'

const Home = () => {
    return (
        <div className="home">
            <div className="home__container">
                <img className="home__image" src="https://s2.adlibris.com/images/61500292/promo1280x270.jpg" alt=" " />
            </div>
            <div className="home__row">
                {/*  Six books */}
                <Books />
            </div>

        </div>
    )
}

export default Home
