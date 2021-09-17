import React from 'react'
import './Book.css'

const Book = () => {
    return (
        <div className="book">
            <img src="https://s1.adlibris.com/images/59263007/valo-joka-ei-kadonnutkaan.jpg" alt="" />
            <div class="book_info">
                <p>The lean startup</p>
                <p className="book_price">
                    <small>€</small>
                    <strong>29.9</strong>
                </p>
            </div>

            <button>Add to Basket</button>
        </div>
    )
}

export default Book
