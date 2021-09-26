import { createSlice } from "@reduxjs/toolkit";

const initialState = []

export const bookstoreSlice = createSlice({
    name: 'bookstore',
    initialState,
    reducers: {
        addToBasket(state, action) {
            state.push(action.payload)
        },
    }
})

export const { addToBasket } = bookstoreSlice.actions

export default bookstoreSlice.reducer