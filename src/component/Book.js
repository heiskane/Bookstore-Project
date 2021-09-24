import React from 'react'
import './Book.css'
import { useDispatch } from 'react-redux';
import { addToBasket } from './slice'

const Book = ({ book }) => {
    const dispatch = useDispatch()

    const saveToBasket = () => {
        if ({ book }) {
            dispatch(
                addToBasket({
                    book
                })
            )
        }
    }

    return (
        <div className="book">
            <img src="https://s1.adlibris.com/images/59263007/valo-joka-ei-kadonnutkaan.jpg" alt="" />
            <div class="book__info">
                <p>Name: {book.title}</p>
                <p>Author: {book.authors[0].name}</p>
                <p className="book_price">Price:
                    <strong> {book.price}</strong>
                    <small> €</small>
                </p>
            </div>
            <button type="button" onClick={saveToBasket}>Add to Basket</button>
        </div>
    )
}

export default Book
